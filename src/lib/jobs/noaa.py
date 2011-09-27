#!/usr/bin/python
import logging
import os
from ftplib import FTP
from datetime import datetime
from jobcontrol import Job
from jobcontrol import Configurable

class FTP2(Job):
    """ A mock-up FTP client """
    def __init__(self, ftphost):
        Job.__init__(self)
        self.remotehost = ftphost
        self.logged_in = False
        self.log.debug("Opened FTP connection to "+ftphost)

    def configure(self):
        Job.configure(self, 'conf/noaajob.conf')

    def login(self):
        self.log.debug("Logged in.")
        self.logged_in = True

    def retrbinary(self, filename, callback):
        self.check()
        callback("Got the contents of " + filename + "\n")

    def close(self):
        self.log.debug("FTP session is closed.")

    def cwd(self, newdir):
        self.check()
        self.log.debug("Changed remote dir to "+newdir)

    def nlst(self, dir='.'):
        self.check()
        self.log.debug("Created a dir listing  of a remote dir "+dir)
        return "\n".join('%dZ.txt' % hour for hour in range(13))

    def check(self):
        if not self.logged_in:
            raise Exception(" Not logged in")

class NoaaCycle:
    @staticmethod
    def current_date():
        """Get a date string for the current cycle
        """
        current_date = datetime.utcnow() 
        if(current_date.hour == 24):
            # 23Z.txt belongs to previous day
            current_date = datetime.utcnow() - datetime.timedelta(1)
        return current_date.strftime("%Y-%m-%d")

    @staticmethod
    def current_date24():
        """Get a date string for the current cycle -- a version for Python 2.4
        """
        current_date = datetime.utcnow() 
        # 2do also decrement when last day of the month, last month of the year
        datestr = current_date.strftime("%Y-%m")
        day = current_date.day()
        if(current_date.hour == 24):
            # 23Z.txt belongs to previous day
            day = (current_date.day() - 1)
        datestr = datestr + "-%02d" % day
        return datestr

    @staticmethod
    def current_file():
        """Get the name of the current cycle file as defined by
        http://weather.noaa.gov/weather/metar.shtml
        The name of a current file is {<UTC hour>-1}Z.TXT
        """
        hour = (23 + int(datetime.utcnow().strftime("%H")))%24
        if hour < 10:
            return "0%dZ.TXT" % hour
        else:
            return "%dZ.TXT" % hour

class NoaaJob(Job):
    """ Get actual data from NOAA METAR cycle files
    """
    def start(self):
        Job.start(self)

    def action(self):
        file = NoaaCycle.current_file()
        local_dir = self.download_dir + '/' + NoaaCycle.current_date24()
        # a mock-up client for a while
        session = FTP2(self.ftp_host)
        self.log.info("Connected to %s" % self.ftp_host)
        self.log.info("Downloading %s/%s" % (self.remote_dir, file))
        try:
            session.login() 
            session.cwd(self.remote_dir)
            self.download(session, local_dir, file)
        except Exception, e:
            self.log.error("%s" % e)
        session.close()
        self.addReport("Downloaded", local_dir + "/" + file)
        self.addReport("status", "complete")

    def download_all(self, session, file):
        # read the filelist
        newfiles = session.nlst()
        self.log.debug("Got a file list: "+newfiles)
        local_dir = self.download_dir + '/' + NoaaCycle.current_date()
        files     = newfiles.splitlines()
        [self.download(session, local_dir, file) for file in files]

    def download(self, session, local_dir, file):
        local_file = local_dir + '/' + file
        if not os.access(local_dir,os.F_OK):
            os.mkdir(local_dir)
        # 2do check if the file already exists
        session.retrbinary('RETR ' + file, open(local_file, 'wb').write)
        file_size = "%dB" % (os.stat(local_file).st_size,)
        self.log.info("Downloaded %s: %s" % (local_file, file_size))

    def configure(self):
        Job.configure(self, 'conf/noaajob.conf')
        self.remote_dir   = self.config.get("noaajob", "remote_dir")
        self.download_dir = self.config.get("noaajob", "download_dir")
        self.ftp_host     = self.config.get("noaajob", "ftp_host")
        
    def __init__(self, code=None):
        Job.__init__(self)

if __name__ == "__main__":
    job = NoaaJob()
    job.start()
    job.report()
# 2do get results, call the next job in queue (upload to database)
