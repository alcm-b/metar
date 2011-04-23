#!/bin/sh
#set -e
export PYTHONPATH=.:/usr/local/lib/python:`pwd`/src/lib

clear
# python ./src/cycle.py
cd src && python ./lib/jobs/noaa.py
tail -n 22 -v ./metarloader.log
