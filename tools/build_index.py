#!/usr/bin/env python3
"""Checks every theme in themes/ and writes index.json, which Q2 Theme Studio reads.

python3 tools/build_index.py

A theme is plain text that the firmware reads through an allowlist, so a bad one can't do harm. This
keeps the library tidy all the same: only the lines a theme can hold, and a name for each. It exits
with an error, and writes nothing, if any file fails, so a pull request's check shows what's wrong."""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
MAX_BYTES = 16384
NAME_MAX = 40
FILE = re.compile(r'[a-z0-9][a-z0-9-]*\.txt')
HEX = r'#[0-9a-fA-F]{6}'
WIDGET = r'[a-z0-9_]{1,40}'
NUMBER = r'-?[0-9]{1,4}'
LINES = tuple(re.compile(line) for line in (
    r'name [^ ].*', r'author [^ ].*', rf'accent {HEX}', rf'color bg {HEX}', r'battery (icon|percent|both|inside)',
    r'page [a-z_]{1,40}', rf'hide {WIDGET}', rf'move {WIDGET} {NUMBER} {NUMBER}', rf'size {WIDGET} {NUMBER} {NUMBER}',
    rf'tint {WIDGET} {HEX}', rf'font {WIDGET} [0-9]{{1,3}}', rf'text {WIDGET} [^ ].*',
))


def check(path):
    """The theme's index entry, or its first problem as a string."""
    if not FILE.fullmatch(path.name):
        return 'the file name must be lower-case letters, digits and dashes, ending .txt'
    raw = path.read_bytes()
    if len(raw) > MAX_BYTES:
        return f'over {MAX_BYTES} bytes'
    try:
        lines = raw.decode('utf-8').removeprefix('﻿').replace('\r\n', '\n').rstrip('\n').split('\n')
    except UnicodeDecodeError:
        return 'not UTF-8 text'
    if lines[0] != 'q2theme 1' or lines[-1] != 'end' or len(lines) < 3:
        return 'a theme starts with q2theme 1 and ends with end'
    found = {}
    for number, line in enumerate(lines[1:-1], 2):
        if any(ord(c) < 32 or ord(c) == 127 for c in line) or not any(rule.fullmatch(line) for rule in LINES):
            return f'line {number} is not a theme line'
        word, _, rest = line.partition(' ')
        if word in ('name', 'author', 'accent'):
            found[word] = rest
        elif word == 'color':
            found['bg'] = rest.split()[1]
    if not 0 < len(found.get('name', '')) <= NAME_MAX:
        return f'a theme needs a name line of at most {NAME_MAX} characters'
    if len(found.get('author', '')) > NAME_MAX:
        return f'an author is at most {NAME_MAX} characters'
    return {'file': path.name, **found}


def main():
    entries, problems = [], []
    for path in sorted((ROOT/'themes').iterdir()):
        result = check(path)
        (problems.append(f'{path.name}: {result}') if isinstance(result, str) else entries.append(result))
    if problems:
        sys.exit('\n'.join(problems))
    entries.sort(key=lambda entry: entry['name'].lower())
    (ROOT/'index.json').write_text(json.dumps({'themes': entries}, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')
    print(len(entries), 'themes')


if __name__ == '__main__':
    main()
