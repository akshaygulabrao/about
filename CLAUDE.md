# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

Akshay Gulabrao's personal website (biotech price targets, notes, blog). Plain markdown source → pandoc → committed HTML, served as a static site by GitHub Pages. The stated philosophy (`index.md`): no static site generator, no framework — "features you don't need are a bug."

## Build / publish

`./build.sh` is the entire toolchain. It:
1. Runs `pandoc <page>.md -o <page>.html --mathjax --css=style.css -s --citeproc` for each page (`index.md` is built without `--citeproc`).
2. `git add`s each `.md`/`.html` pair explicitly, plus `build.sh` and `media/*`.
3. `git commit -m "update"` and `git push`.

Deploy is automatic: `.github/workflows/static.yml` uploads the entire repo to GitHub Pages on every push to `main`. There is no test suite, linter, or CI build step — pushing the rendered HTML *is* the deploy.

## Adding a new page

Every page must be wired in four places, or it won't ship:
1. Create `<slug>.md` with YAML frontmatter (`title`, `author`, `date`, and `bibliography: library.bib` if it cites anything). Start the body with `[Home](./index.html)` and a `---`.
2. Add a `pandoc <slug>.md -o <slug>.html ...` line to `build.sh` (use `--citeproc` if it has citations).
3. Add `git add <slug>.md <slug>.html` to `build.sh`.
4. Link to `<slug>.html` from `index.md` under the appropriate section (Biotech Price Targets / Notes / Blog).

## Citations

Posts use pandoc citeproc with `.bib` files (`library.bib` shared, or post-specific like `abvx_references.bib`). Important: `.gitignore` excludes `*bib`, so **bib files are local-only**. The rendered citations are baked into the committed HTML — anyone cloning the repo cannot rebuild a cited page without re-creating the bibliography. Treat `.bib` files as build inputs that live only on the author's machine.

## Conventions worth matching

- Commit messages are literally `update`. Don't introduce a different style unless asked.
- `style.css` is intentionally tiny (~10 lines). Don't expand it speculatively.
- Each post links back to `./index.html` via a top-of-page `[Home]` link followed by `---`.
- Images go in `media/` and are referenced as `./media/<file>`.
