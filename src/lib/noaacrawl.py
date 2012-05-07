#!/usr/bin/python
from jobs.noaa import NoaaJob
from jobs.archive import ArchiveJob
job = NoaaJob()
job.start()
job.report()

# put monthly reports into zip
# job = ArchiveJob()
# job.start()
