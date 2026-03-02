#!/usr/bin/env bash

set -e

export NODE_OPTIONS=--openssl-legacy-provider

npm run github:build

cd docs/.vuepress/github

git init
git add -A
git commit -m 'deploy'
git branch -M main

git push -f https://github.com/Tskysheep/english-grammar-book.git main:gh-pages

cd -
