#!/bin/sh
set -e
. ./ref
. ./ref.local
export PYTHONPATH=.:/usr/local/lib/python:lib
cd $MIRRORAPPHOME
python lib/jobs/noaa.py
