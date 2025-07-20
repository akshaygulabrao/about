#!/bin/sh
for f in *.md; do
  pandoc "$f" -o "${f%.md}.html" \
        --mathjax --css=style.css -s
done