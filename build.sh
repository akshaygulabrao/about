#!/bin/sh
pandoc index.md -o "index.html" --mathjax --css=style.css -s
pandoc supply-chains.md -o supply-chains.html --mathjax --css=style.css -s --citeproc
pandoc lottery_EV.md -o lottery_EV.html --mathjax --css=style.css -s --citeproc

git add index.md index.html
git add supply-chains.md supply-chains.html
git add lottery_EV.md lottery_EV.html

git add build.sh

git commit -m "update"
git push
