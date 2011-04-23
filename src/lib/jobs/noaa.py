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
        self.log.debug("Opened FTP connection to "+ftphost)

    def configure(self):
        Job.configure(self, 'conf/noaajob.conf')

    def login(self):
        self.log.debug("Logged in.")
        self.logged_in = True

    def retrlines(self, filename, callback):
        callback("Got the contents of " + filename + "\n")

    def close(self):
        self.log.debug("FTP session is closed.")

    def cwd(self, newdir):
# TODO bail out if not logged in
        self.log.debug("Changed remote dir to "+newdir)

    def nlst(self, dir='.'):
        self.log.debug("Created a dir listing  of a remote dir "+dir)
        return "\n".join('%dZ.txt' % hour for hour in range(13))

class NoaaCycle:
    @staticmethod
    def current_date():
        """Get a date string for the current cycle
        """
        return datetime.utcnow().strftime("%Y-%m-%d");

    @staticmethod
    def current_file():
        """Get the name of the current cycle file as defined by
        http://weather.noaa.gov/weather/metar.shtml
        The name of a current file is [<UTC hour> - 1]Z.TXT
        """
        hour = (23 + int(datetime.utcnow().strftime("%H")))%24;
        return "%dZ.TXT" % hour

class NoaaJob(Job):
    """ Get actual data from NOAA METAR cycle files
    """
    def start(self):
        Job.start(self)

    def action(self):
        self.log.debug("Downloading from URL: "+self.remote_dir)
        # a mock-up client for a while
        session = FTP2(self.ftp_host)
        self.log.info("Connected to %s" % self.ftp_host)
        try:
            session.login() 
            session.cwd(self.remote_dir)
            # download the current file:
            local_dir = self.download_dir + '/' + NoaaCycle.current_date()
            file      = NoaaCycle.current_file()
            self.download(session, local_dir, file)
            session.close()
        except Exception as e:
            self.log.error("%s" % e)

    def download_all(self, session, file):
        # read the filelist
        newfiles = session.nlst()
        self.log.debug("Got a file list: "+newfiles)
        local_dir = self.download_dir + '/' + NoaaCycle.current_date()
        files     = newfiles.splitlines()
        [self.download(session, local_dir, file) for file in files]

    def download(self, session, local_dir, file):
        local_file = local_dir + '/' + file
        self.log.debug("Downloading %s " % (file,))
        if not os.access(local_dir,os.F_OK):
            os.mkdir(local_dir)
        # 2do check if the file already exists
        session.retrlines('RETR '+file, open(local_file, 'wb').write)
        file_size = "%dB" % (os.stat(local_file).st_size,)
        self.log.info("Downloaded %s: %s" % (local_file, file_size))

    def configure(self):
        Job.configure(self, 'conf/noaajob.conf')
        self.remote_dir = self.config.get("noaajob", "remote_dir")
        self.download_dir = self.config.get("noaajob", "download_dir")
        self.ftp_host = self.config.get("noaajob", "ftp_host")
        
    def __init__(self, code=None):
        Job.__init__(self)

if __name__ == "__main__":
    job = NoaaJob()
    job.start()
