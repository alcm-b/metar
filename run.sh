#!/bin/sh
#set -e
export PYTHONPATH=.:/usr/local/lib/python:`pwd`/src/lib
cd src && python ./lib/jobs/noaa.py
