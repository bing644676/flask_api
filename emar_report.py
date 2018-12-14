#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys
import getopt
import logging
import logging.handlers
from emar_config import *
from emar_mysql import DbMysql


def initlog(LOG_FILE):
    loginstance = logging.getLogger()
    hdlr = logging.handlers.TimedRotatingFileHandler(LOG_FILE, when='H', interval=1, backupCount=40)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    loginstance.addHandler(hdlr)
    loginstance.setLevel(logging.NOTSET)
    return loginstance

log_file = './log/emar_report.log'

