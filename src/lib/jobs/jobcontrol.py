#!/usr/bin/python
import logging
import ConfigParser
from reporting.logger import Logger

class Configurable:
    def configure(self, filename=None):
        self.config = ConfigParser.ConfigParser()
        if None != filename:
            self.config.read(filename)

    def __init__(self):
        self.configure()

class Reportable:
    """Collect reporting data and output it on demand
    TODO: consider make it a wrapper of a logger object
    """
    reportItems = {'Started':''}
    def addReport(self, name, value):
        self.reportItems[name] = value

    def report(self):
        print "\n".join(["%s: %s" % (k, v) for k, v in self.reportItems.items()])

# start, stop, status
class Job(Configurable, Reportable):
    """Run an asynchronous task"""
    def start(self):
        self.log.info('Started')
        try:
            self.action()
        except RuntimeError, e:
            self.log.error("%s" % e)
         #self.report()

    def action(self):
        """The task to be performed, empty by default"""
        pass

    def configure(self, filename):
        Configurable.configure(self, filename)

    def __init__(self):
        Configurable.__init__(self)
        Logger.initialize("metarloader")
        self.log = logging.getLogger("metarloader")
