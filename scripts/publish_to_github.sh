#!/usr/bin/env bash
# One-command fallback for publishing this repo to GitHub when the `gh` CLI
# isn't installed. Run this from the project root:
#
#   bash scripts/publish_to_github.sh
#
# It will:
#   1. Ask for your GitHub username and the repo name you want to create
#   2. Walk you through creating an empty repo on github.com (since we can't
#      do that for you without the gh CLI)
#   3. Add it as a git remote and push your existing commits
#
# Safe to re-run: if the remote already exists it will just push.

set -euo pipefail

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "This doesn't look like a git repository yet."
  echo "Run 'git init' and commit your work first, then re-run this script."
  exit 1
fi

echo "== Publish this project to GitHub =="
echo
read -rp "Your GitHub username: " GH_USER
read -rp "Repository name to create (e.g. python-coding-trainer): " REPO_NAME

if [ -z "$GH_USER" ] || [ -z "$REPO_NAME" ]; then
  echo "Username and repo name are required."
  exit 1
fi

REMOTE_URL="https://github.com/${GH_USER}/${REPO_NAME}.git"

if ! git remote get-url origin >/dev/null 2>&1; then
  echo
  echo "Before continuing, create an EMPTY repository on GitHub:"
  echo "  1. Go to https://github.com/new"
  echo "  2. Repository name: ${REPO_NAME}"
  echo "  3. Do NOT initialize with a README, .gitignore, or license"
  echo "     (this project already has those files)"
  echo "  4. Click 'Create repository'"
  echo
  read -rp "Press Enter once you've created the repo on GitHub..." _

  git remote add origin "$REMOTE_URL"
  echo "Added remote 'origin' -> $REMOTE_URL"
else
  echo "Remote 'origin' already configured: $(git remote get-url origin)"
fi

CURRENT_BRANCH="$(git symbolic-ref --short HEAD 2>/dev/null || echo main)"
echo
echo "Pushing branch '$CURRENT_BRANCH' to GitHub..."
git push -u origin "$CURRENT_BRANCH"

echo
echo "Done! Your repo is live at:"
echo "  https://github.com/${GH_USER}/${REPO_NAME}"
