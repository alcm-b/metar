#!/bin/sh
#set -e
export PYTHONPATH=.:/usr/local/lib/python:src/lib

clear
# python ./src/cycle.py
python ./src/lib/jobs/noaa.py
tail -n 22 -v ./metarloader.log
