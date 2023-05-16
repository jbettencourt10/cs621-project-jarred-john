#!/bin/bash

if [[ $# -ne 6 ]]; then
  echo "USAGE: make run FILE=filename";
  exit;
fi

# Insert preprocessing here:
. venv/bin/activate
python3 src/runner.py "$@"