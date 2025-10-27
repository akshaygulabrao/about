#!/bin/sh
# for f in *.md; do
#   pandoc "$f" -o "${f%.md}.html" \
#         --mathjax --css=style.css -s
# done

pandoc index.md -o "index.html" --mathjax --css=style.css -s
pandoc abvx.md -o abvx.html --mathjax --css=style.css -s --citeproc
pandoc eq.md -o eq.html --mathjax --css=style.css -s --citeproc
pandoc growth-stock-screener.md -o growth-stock-screener.html --mathjax --css=style.css -s --citeproc
pandoc capr.md -o capr.html --mathjax --css=style.css -s --citeproc



git add index.md index.html
git add abvx.md abvx.html
git add eq.md eq.html
git add capr.md capr.html
git add growth-stock-screener.md growth-stock-screener.html


git add build.sh
git add media/*

git commit -m "update"
git push