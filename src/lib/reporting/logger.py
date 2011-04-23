#!/usr/lib/python
import logging
import sys

class Logger:
    initialized = {}
    @staticmethod
    def initialize(logger_name='out'):
        if not logger_name in Logger.initialized:
            # formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            formatter = logging.Formatter("[%(asctime)s] %(levelname)s : %(message)s")
            fh = logging.FileHandler(logger_name + ".log")
            fh.setLevel(logging.DEBUG)
            fh.setFormatter(formatter)
            fh2 = logging.StreamHandler(sys.stdout)
            fh2.setLevel(logging.INFO)
            fh2.setFormatter(formatter)
            logger = logging.getLogger(logger_name)
            logger.setLevel(logging.DEBUG)
            logger.addHandler(fh)
            logger.addHandler(fh2)
            Logger.initialized[logger_name] = 1

    def _simpleLogger(self):
        LOG_FILENAME = 'example.log'
        logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
        logging.debug('This message goes to the log file')
