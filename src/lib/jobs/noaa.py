import os
from ftplib import FTP
from jobcontrol import Job
from export.noaa import NoaaCycle
from utility.ftp2 import FTP2

class NoaaJob(Job):
    """ Get actual data from NOAA METAR cycle files
    """
    def start(self):
        Job.start(self)

    def action(self):
        file = NoaaCycle.current_file()
        local_dir = self.download_dir + '/' + NoaaCycle.current_date()
        # 2do select FTP client depending on configuration (development|production)
        # mock-up client for a while
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
