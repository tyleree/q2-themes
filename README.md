# Q2 themes

Themes for the Shanling Q2 running Q2 Pod firmware, shared by the people who made them. Q2 Theme Studio shows them
in its **Library** tab.

**Q2 Theme Studio runs in your browser: <https://tyleree.github.io/q2-themes/>.** In Chrome or Edge it writes straight to
the Q2's card once you choose it. Firefox and Safari can't write to a card, so there you export a file and copy it over.

Themes only show on a Q2 running the card themes test firmware, a
[pre-release on the fork](https://github.com/tyleree/q2-pod/releases/tag/card-themes-test-1). Official Q2 Pod does not
read them yet. The Studio's EQ tab works on any Q2 Pod.

## Use a theme

In Q2 Theme Studio, open **Library**, click a theme, change it if you like, and press **Save to Q2**.

## Share a theme

In Q2 Theme Studio, give your theme a name, open **Library** and press **Share this theme**. A GitHub page opens with your
theme filled in. Press **Propose changes**, then **Create pull request**. You need a free GitHub account.

A check runs on every submission. Once it passes and a maintainer has merged it, the theme appears in the Library within a
few minutes. Please keep names friendly, and don't reuse someone else's without saying where it came from.

By sharing a theme you agree that anyone may use, change and share it, under [CC0](https://creativecommons.org/publicdomain/zero/1.0/).

## What a theme is

`themes/<name>.txt` is one theme, in the format in the test firmware's [docs/themes.md](https://github.com/tyleree/q2-pod/blob/feature/card-themes/docs/themes.md).
It's plain text, and the firmware only acts on an allowlist of lines, so a theme can't run anything. `index.json` is written
by `tools/build_index.py`, and a push to `main` rebuilds it, so don't edit it by hand.

## The Studio's files

`docs/` is the Studio as GitHub Pages serves it. Its source is `tools/theme-studio/ui` on the
[card themes branch](https://github.com/tyleree/q2-pod/tree/feature/card-themes). The EQ tab's headphone presets are
[AutoEq](https://github.com/jaakkopasanen/AutoEq)'s published results, under its MIT licence (`docs/AUTOEQ-LICENSE.txt`).
