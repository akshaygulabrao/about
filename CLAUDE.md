# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

Akshay Gulabrao's personal site. Hugo static site, **PaperMod** theme, deployed to GitHub Pages at `https://akshaygulabrao.github.io/about/`. Migrated from a hand-rolled pandoc setup — the philosophy shifted from "minimum tooling" to "whatever the LLM can maintain efficiently with the most training data behind it," which is why Hugo was chosen over Quarto or the original pandoc pipeline.

## Build / publish

- **Local preview:** `hugo server` (or `hugo --minify` for a one-shot build into `public/`).
- **Deploy:** push to `main`. `.github/workflows/static.yml` installs Hugo, builds with `hugo --minify`, and uploads `./public` to GitHub Pages. No build artifacts are committed; `public/`, `resources/`, and `.hugo_build.lock` are gitignored.
- **Hugo version** is pinned to `0.161.1` in the workflow (`env: HUGO_VERSION`). If you bump it, also bump the local install (`brew upgrade hugo`).

## Theme: PaperMod

- Added as a git submodule at `themes/PaperMod` tracking `master`. When cloning fresh: `git submodule update --init --recursive`.
- Requires Hugo ≥ 0.146 (enforced by the theme via `layouts/baseof.html`).
- Site config in `hugo.toml`. Homepage intro (the struck-through preamble + the LLM line + email) lives in `[params.homeInfoParams].Content` — edit there, **not** in a content file.

## Adding a new post

1. `hugo new content posts/<slug>.md` — or just create `content/posts/<slug>.md` directly.
2. Frontmatter (TOML or YAML both work; existing posts use YAML):
   ```yaml
   ---
   title: "..."
   date: 2026-MM-DD
   draft: false
   tags: ["..."]
   math: true   # only if the post uses LaTeX math
   ---
   ```
3. Preview with `hugo server`, then commit and push. No index updating needed — PaperMod auto-lists posts.

## Conventions worth matching

- Commit messages have historically been `update`. There's no enforced style; use whatever is informative.
- The previous setup used pandoc's `--citeproc` with `.bib` files. The current posts have no citations, and the plan going forward is to put references as a manual links list at the bottom of each post rather than re-introduce BibTeX. `*bib` remains gitignored.
- The old `[Home](./index.html)` link pattern at the top of each post is gone — PaperMod provides its own breadcrumb/nav.
