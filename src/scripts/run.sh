#!/bin/bash

if [[ $# -ne 5 ]]; then
  echo "USAGE: make run FILE=filename";
  exit;
fi

# Insert preprocessing here:
. venv/bin/activate
python3 src/runner.py "$@"