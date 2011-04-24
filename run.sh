#!/bin/sh
#set -e
export PYTHONPATH=.:/usr/local/lib/python:lib
cd /home/dayzero0/bin/metar && python lib/jobs/noaa.py
