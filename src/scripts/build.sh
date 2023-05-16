#!/bin/bash

if [[ -e "venv" ]]; then
  echo "Already built";
else
  echo "Creating Virtual Environment...";
  python3 -m venv venv;
  . venv/bin/activate
  echo "Installing Dependencies...";
  pip install -r requirements.txt
  echo "Done!";
fi