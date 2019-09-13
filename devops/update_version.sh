#!/bin/sh

git config --global user.name github-actions[bot]
git remote set-url origin "https://github-actions[bot]:${GITHUB_TOKEN}@github.com/OLBEA20/twelve-step.git"

python3 update_version.py
git add version.txt
git commit -m "Updated version to $(cat version.txt)"
git  push origin HEAD:master