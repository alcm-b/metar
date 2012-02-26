#!/bin/sh
set -e
export PYTHONPATH=.:/usr/local/lib/python:src/lib

# clear
make clean
echo
python ./src/lib/noaacrawl.py
echo
tail -n 22 -v ./metarloader.log
