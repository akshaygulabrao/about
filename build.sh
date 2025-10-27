#!/bin/sh
# for f in *.md; do
#   pandoc "$f" -o "${f%.md}.html" \
#         --mathjax --css=style.css -s
# done

pandoc index.md -o "index.html" --mathjax --css=style.css -s
pandoc abvx.md -o abvx.html --mathjax --css=style.css -s --citeproc
pandoc eq.md -o eq.html --mathjax --css=style.css -s --citeproc
pandoc supply-chains.md -o supply-chains.html --mathjax --css=style.css -s --citeproc
pandoc capr.md -o capr.html --mathjax --css=style.css -s --citeproc
pandoc sprb.md -o sprb.html --mathjax --css=style.css -s --citeproc
pandoc avxl.md -o avxl.html --mathjax --css=style.css -s --citeproc



git add index.md index.html
git add abvx.md abvx.html
git add avxl.md avxl.html
git add eq.md eq.html
git add capr.md capr.html
git add sprb.md sprb.html
git add supply-chains.md supply-chains.html


git add build.sh
git add media/*

git commit -m "update"
git push