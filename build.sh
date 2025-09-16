#!/bin/sh
# for f in *.md; do
#   pandoc "$f" -o "${f%.md}.html" \
#         --mathjax --css=style.css -s
# done

pandoc index.md -o "index.html" --mathjax --css=style.css -s
pandoc voice_fake.md -o "voice_fake.html" --mathjax --css=style.css -s --citeproc
pandoc abvx.md -o abvx.html --mathjax --css=style.css -s --citeproc
pandoc nursing.md -o nursing.html --mathjax --css=style.css -s --citeproc

git add index.md index.html
git add voice_fake.md voice_fake.html
git add abvx.md abvx.html
git add nursing.md nursing.html
