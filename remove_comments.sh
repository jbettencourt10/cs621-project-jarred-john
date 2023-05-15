#!/bin/bash

if [ "$#" -ne 1 ]; then
  echo "Expected exactly one argument, which is the filename for which comments should be removed."
  exit 1
fi

gcc -fpreprocessed -dD -E "$1" -o "${1}.nocomments"