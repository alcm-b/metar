#!/bin/sh
#set -e
export PYTHONPATH=.:/usr/local/lib/python:src/lib
cd home/dayzero0/bin/metar && python ./src/lib/jobs/noaa.py
