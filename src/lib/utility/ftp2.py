from jobs.jobcontrol import Job

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
