#!/bin/bash

if [[ $# -ne 5 ]]; then
  echo "USAGE: make run FILE=filename";
  exit;
fi

# Insert preprocessing here:
src/scripts/remove_comments.sh "$5"
. venv/bin/activate
python3 src/runner.py "$@"