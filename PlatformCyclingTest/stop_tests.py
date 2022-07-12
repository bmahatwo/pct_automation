#!/usr/bin/python

import datetime
import difflib
import logging
import json
import os
import shutil
import sys
import subprocess
import time
from subprocess import Popen, PIPE
from inspect import currentframe, getframeinfo

""" Import constants for usage"""
import constants

""" Import functions for usage"""
import execute_save_compare

""" Create frame object """
frameObj = currentframe()

""" Get current file name """
fileName = str(os.path.basename(__file__)) 

""" String to track current function name for main function """
functionName = str (__name__)

try:
	logging.basicConfig(filename=constants.LOG_FILE, level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')
except (FileNotFoundError,OSError, IOError) as exception:
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))
	exit()

logger = logging.getLogger(__name__)

logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": SCRIPT_VERSION: " + constants.SCRIPT_VERSION)

if __name__ == '__main__':
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": this is main")
else:
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": this is NOT main")

""" We remove this file here too, in case tests are not properly finished """
if os.path.exists (constants.CONF_FILE_ETC_INIT):
	try:
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file exists: " + constants.CONF_FILE_ETC_INIT)
		os.remove (constants.CONF_FILE_ETC_INIT)
		print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": removed " + constants.CONF_FILE_ETC_INIT)
	except (OSError, IOError) as exception:
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))
else:
	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file does not exist: " + constants.CONF_FILE_ETC_INIT)

execute_save_compare.save_error_summary()

logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": After calling save_error_summary()")
