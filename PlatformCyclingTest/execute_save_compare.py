#!/usr/bin/python

import datetime
import difflib
import filecmp
import logging
import json
import os
import requests
import shutil
import sys
import subprocess
import time
from subprocess import Popen, PIPE, TimeoutExpired
from inspect import currentframe, getframeinfo

""" Import constants for usage"""
import constants

""" Create frame object """
frameObj = currentframe()

""" Get current file name """
fileName = str(os.path.basename(__file__)) 

""" String to track current function name for main function """
functionName = str (__name__)

if __name__ == '__main__':
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": this is main")
else:
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": this is NOT main")

if not os.path.isdir(constants.LOG_DIRECTORY_FULL_PATH):
	try:
		print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": directory does not exist: " + constants.LOG_DIRECTORY_FULL_PATH)
		os.mkdir(constants.LOG_DIRECTORY_FULL_PATH)
		print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": directory created: " + constants.LOG_DIRECTORY_FULL_PATH)
	except (FileNotFoundError,OSError, IOError) as exception:
		print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

		print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": exiting script")
		exit()

logger = logging.getLogger(__name__)

logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": SCRIPT_VERSION: " + constants.SCRIPT_VERSION)

# Ensure that python at least 3.0 is used
if sys.version_info < (3,0):
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": error: Test requires python 3.x")
	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: Test requires python 3.x")
	exit()

def execute_Command(commandString):
	"""
	Purpose: To execute given command

	Parameters: String command

	Returns: String output
	"""

	""" Create frame object """
	frameObj = currentframe()

	""" String to track current function name """
	functionName = str(frameObj.f_code.co_name) + "()" # Function name

	# store starting time
	startTime = time.time()

	try:
		status = subprocess.check_output(commandString + " 2>/dev/null", stderr= subprocess.STDOUT, shell=True, universal_newlines=True, timeout=constants.COMMAND_TIMELIMIT)

		# Enable these prints to debugging commands execution taking more time
		# logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": commandString: " + str(commandString))
		# logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": status: " + str(status))

		return status

	except (TimeoutExpired) as exception:
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": commandString: " + commandString)
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": exception: " + str(exception))
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": exception.output: " + str(exception.output))
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": exception.cmd: " + str(exception.cmd))

	except (FileNotFoundError, OSError, IOError, subprocess.CalledProcessError) as exception:
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": commandString: " + commandString)
		# logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": exception: " + str(exception))
		# logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": exception.returncode: " + str(exception.returncode))
		# logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": exception.cmd: " + str(exception.cmd))

	# store end time
	endTime = time.time()

	if (int(endTime-startTime) > 0):
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": commandString: " + commandString)
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Time taken for function execution: " + str(int(endTime-startTime)))

def copy_file_to_iteration_folder(iterationFolderCompletePath):
	"""
	Purpose: To copy desired file from given location to iteration folder

	Parameters:
	iterationFolderCompletePath: String: indicates iteration folder name. This includes complete path

	Returns: None
	"""

	""" Create frame object """
	frameObj = currentframe()

	""" String to track current function name """
	functionName = str(frameObj.f_code.co_name) + "()" # Function name

	# store starting time
	startTime = time.time()

	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Entered")

	if os.path.isdir(iterationFolderCompletePath):
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": directory exists: " + iterationFolderCompletePath)
	else:
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": directory does not exist: " + iterationFolderCompletePath)
		return

	if os.path.isfile(constants.JSON_CONFIG_FILE_COPY_DUT_FILES):
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file exists: " + constants.JSON_CONFIG_FILE_COPY_DUT_FILES)
	else:
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file does not exist: " + constants.JSON_CONFIG_FILE_COPY_DUT_FILES)
		return

	try:
		# Iterating through the json file. it is dict of dict
		with open(constants.JSON_CONFIG_FILE_COPY_DUT_FILES) as fileObjectJSONCopyFiles:
			dataCopyDUTFiles = json.load(fileObjectJSONCopyFiles)

			# Iterating through the json dict
			for dut_path_file in dataCopyDUTFiles['copy_log_files_for_iteration']:
				stop_on_error_String = dataCopyDUTFiles['copy_log_files_for_iteration'][dut_path_file]

				if os.path.isfile(dut_path_file):
					shutil.copy(dut_path_file, iterationFolderCompletePath)
				else:
					logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file does not exist: " + dut_path_file)

				if (stop_on_error_String != "STOP_ON_ERROR_NO"):
					logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": before writing file for stop_on_error for: " + str(dut_path_file))

					try:
						with open(constants.STOP_ON_ERROR_FILE,"w") as fileObjectStopOnError:
							fileObjectStopOnError.write (str("STOP_ON_ERROR"))

					except (OSError, IOError) as exception:
						logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

					logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": after writing files for stop_on_error")

	except (OSError, IOError, KeyError, json.decoder.JSONDecodeError) as exception:
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": exception: " + str(exception))

		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": exiting script")
		exit()

	# store end time
	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Calling sync")
	execute_Command("sync")
	endTime = time.time()

	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Time taken for function execution: " + str(int(endTime-startTime)))

def retain_log_files(iterationFolderCompletePath):
	"""
	Purpose: To create log file to indicate log files are to be retained

	Parameters:
	targetValue: integer value to indicate the timestamp

	Returns: None
	"""
	""" Create frame object """
	frameObj = currentframe()

	""" String to track current function name """
	functionName = str(frameObj.f_code.co_name) + "()" # Function name

	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Entered")

	if not os.path.exists(constants.RETAIN_LOG_FILES):
		try:
			with open(constants.RETAIN_LOG_FILES,"w") as fileObjectRetainLogFiles:
				fileObjectRetainLogFiles.write (str("RETAIN_LOG_FILES"))

				logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": after writing file for RETAIN_LOG_FILES")

		except (OSError, IOError) as exception:
			logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

def measure_time_between_each_iteration(targetValue, iterationFolderCompletePath):
	"""
	Purpose: To measure time taken between each iteration

	Parameters:
	targetValue: integer value to indicate the timestamp

	Returns: None
	"""

	""" Create frame object """
	frameObj = currentframe()

	""" String to track current function name """
	functionName = str(frameObj.f_code.co_name) + "()" # Function name

	# store starting time
	startTime = time.time()

	if os.path.isdir(constants.LOG_DIRECTORY_FULL_PATH):
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": directory exists: " + constants.LOG_DIRECTORY_FULL_PATH)
	else:
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": directory does not exist: " + constants.LOG_DIRECTORY_FULL_PATH)
		return

	# time() function returns the number of seconds passed since epoch
	# currentTimestampString = int (time.time())
	currentTimestampString = int(datetime.datetime.now().timestamp())

	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": current timestamp: " + str(int(currentTimestampString)))

	if os.path.isfile(constants.PREVIOUS_TIMESTAMP_FILE):
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file exists: " + constants.PREVIOUS_TIMESTAMP_FILE)

		try:
			previousTimestamp = 0
			if os.stat(constants.PREVIOUS_TIMESTAMP_FILE).st_size != 0:
				with open(constants.PREVIOUS_TIMESTAMP_FILE,"r") as fileObjectPreviousTimestamp:
					previousTimestamp = int (fileObjectPreviousTimestamp.read())

			timeDifference = currentTimestampString - previousTimestamp

			logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": previousTimestamp: " + str(previousTimestamp))
			logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": targetValue: " + str(targetValue))
			logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": timeDifference: " + str(timeDifference))

			if (timeDifference > targetValue and timeDifference < 0):
				logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): timeDifference (seconds) is more than " + str(targetValue) + " or timeDifference is less than 0. timeDifference: " + str(timeDifference))
				append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ":\t" + iterationFolderCompletePath + "\t" + ": FOR PCT TRACKING: ERROR: Time between iterations is more than " + str(targetValue) + " seconds or less than 0" + "\n", os.path.join(constants.LOG_DIRECTORY_FULL_PATH, constants.ERROR_DETAILS_FILE))
				retain_log_files(iterationFolderCompletePath)
			else:
				logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": timeDifference (seconds) is less than " + str(targetValue))

		except (OSError, IOError) as exception:
			logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

	else:
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file does not exists: " + constants.PREVIOUS_TIMESTAMP_FILE)

	# This is one-time writing the content, and not append operation
	write_string_to_file(str(currentTimestampString), constants.PREVIOUS_TIMESTAMP_FILE)

	# store end time
	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Calling sync")
	execute_Command("sync")
	endTime = time.time()

	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Time taken for function execution: " + str(int(endTime-startTime)))

def clear_older_crash_log_files():
	"""
	Purpose: To clear off older crash log files

	Parameters: None

	Returns: None
	"""

	""" Create frame object """
	frameObj = currentframe()

	""" String to track current function name """
	functionName = str(frameObj.f_code.co_name) + "()" # Function name

	# store starting time
	startTime = time.time()

	if os.path.isdir(constants.LOG_DIRECTORY_FULL_PATH):
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": directory exists: " + constants.LOG_DIRECTORY_FULL_PATH)
	else:
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": directory does not exist: " + constants.LOG_DIRECTORY_FULL_PATH)
		return

	# time() function returns the number of seconds passed since epoch
	currentTimestampString = int(datetime.datetime.now().timestamp())

	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": timestamp: " + str(int(currentTimestampString)))

	# Refer this link: https://chromium.googlesource.com/chromiumos/platform2/+/master/crash-reporter/docs/design.md
	try:
		if os.path.exists ("/sys/kernel/debug/preserved/kcrash"):
			logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": crash error file exists: /sys/kernel/debug/preserved/kcrash")
			os.remove("/sys/kernel/debug/preserved/kcrash")

		if os.path.isdir ("/var/spool/crash"):
			for file in os.listdir("/var/spool/crash"):
				if file.endswith(".bios_log"):
					logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": crash error file exists: " + str(os.path.join("/var/spool/crash/", file)))
					os.remove(os.path.join("/var/spool/crash", file))

				if file.endswith(".dmp"):
					logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": crash error file exists: " + str(os.path.join("/var/spool/crash/", file)))
					os.remove(os.path.join("/var/spool/crash", file))

				if file.endswith(".kcrash"):
					logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": crash error file exists: " + str(os.path.join("/var/spool/crash/", file)))
					os.remove(os.path.join("/var/spool/crash", file))

		if os.path.isdir ("/var/log"):
			for file in os.listdir("/var/log"):
				if file.startswith ("iwl") and file.endswith(".tgz"):
					logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": crash error file exists: " + str(os.path.join("/var/log", file)))
					os.remove(os.path.join("/var/log/", file))

		if os.path.isdir ("/home/chronos/user/crash"):
			for file in os.listdir("/home/chronos/user/crash"):
				if file.endswith(".dmp"):
					logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": crash error file exists: " + str(os.path.join("/home/chronos/user/crash", file)))
					os.remove(os.path.join("/home/chronos/user/crash", file))

				if file.endswith(".core"):
					logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": crash error file exists: " + str(os.path.join("/home/chronos/user/crash", file)))
					os.remove(os.path.join("/home/chronos/user/crash", file))

				if file.endswith(".meta"):
					logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": crash error file exists: " + str(os.path.join("/home/chronos/user/crash", file)))
					os.remove(os.path.join("/home/chronos/user/crash", file))

		if os.path.isdir ("/sys/fs/pstore"):
			for file in os.listdir("/sys/fs/pstore"):
				logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": crash error file exists: " + str(os.path.join("/sys/fs/pstore", file)))
				os.remove(os.path.join("/sys/fs/pstore", file))

		if os.path.isdir ("/dev/pstore"):
			for file in os.listdir("/dev/pstore"):
				logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": crash error file exists: " + str(os.path.join("/dev/pstore", file)))
				os.remove(os.path.join("/dev/pstore", file))

	except (OSError, IOError, KeyError) as exception:
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

	# store end time
	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Calling sync")
	execute_Command("sync")
	endTime = time.time()

	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Time taken for function execution: " + str(int(endTime-startTime)))

def copy_crash_log_files(iterationFolderCompletePath):
	"""
	Purpose: To copy crash log files

	Parameters:
	iterationFolderCompletePath: String: indicates iteration folder name. This includes complete path

	Returns: None
	"""

	""" Create frame object """
	frameObj = currentframe()

	""" String to track current function name """
	functionName = str(frameObj.f_code.co_name) + "()" # Function name

	# store starting time
	startTime = time.time()

	# time() function returns the number of seconds passed since epoch
	currentTimestampString = int(datetime.datetime.now().timestamp())

	if os.path.isdir(constants.LOG_DIRECTORY_FULL_PATH):
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": directory exists: " + constants.LOG_DIRECTORY_FULL_PATH)
	else:
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": directory does not exist: " + constants.LOG_DIRECTORY_FULL_PATH)
		return

	if os.path.isdir(iterationFolderCompletePath):
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": directory exists: " + iterationFolderCompletePath)
	else:
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": directory does not exist: " + iterationFolderCompletePath)
		return

	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": timestamp: " + str(int(currentTimestampString)))

	# Refer this link: https://chromium.googlesource.com/chromiumos/platform2/+/master/crash-reporter/docs/design.md
	try:
		if os.path.exists ("/sys/kernel/debug/preserved/kcrash"):
			logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": crash error file exists: /sys/kernel/debug/preserved/kcrash")
			shutil.copy("/sys/kernel/debug/preserved/kcrash", iterationFolderCompletePath)
			os.remove("/sys/kernel/debug/preserved/kcrash")

		if os.path.isdir ("/var/spool/crash"):
			for file in os.listdir("/var/spool/crash"):
				if file.endswith(".bios_log"):
					logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": crash error file exists: " + str(os.path.join("/var/spool/crash/", file)))
					shutil.copy(os.path.join("/var/spool/crash", file), iterationFolderCompletePath)
					os.remove(os.path.join("/var/spool/crash", file))

				if file.endswith(".dmp"):
					logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": crash error file exists: " + str(os.path.join("/var/spool/crash/", file)))
					shutil.copy(os.path.join("/var/spool/crash", file), iterationFolderCompletePath)
					os.remove(os.path.join("/var/spool/crash", file))

				if file.endswith(".kcrash"):
					logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": crash error file exists: " + str(os.path.join("/var/spool/crash/", file)))
					shutil.copy(os.path.join("/var/spool/crash", file), iterationFolderCompletePath)
					os.remove(os.path.join("/var/spool/crash", file))

		if os.path.isdir ("/var/log"):
			for file in os.listdir("/var/log"):
				if file.startswith ("iwl") and file.endswith(".tgz"):
					logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": crash error file exists: " + str(os.path.join("/var/log", file)))
					shutil.copy(os.path.join("/var/log", file), iterationFolderCompletePath)
					os.remove(os.path.join("/var/log", file))

		if os.path.isdir ("/home/chronos/user/crash"):
			for file in os.listdir("/home/chronos/user/crash"):
				if file.endswith(".dmp"):
					logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": crash error file exists: " + str(os.path.join("/home/chronos/user/crash", file)))
					shutil.copy(os.path.join("/home/chronos/user/crash", file), iterationFolderCompletePath)
					os.remove(os.path.join("/home/chronos/user/crash", file))

				if file.endswith(".core"):
					logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": crash error file exists: " + str(os.path.join("/home/chronos/user/crash", file)))
					shutil.copy(os.path.join("/home/chronos/user/crash", file), iterationFolderCompletePath)
					os.remove(os.path.join("/home/chronos/user/crash", file))

				if file.endswith(".meta"):
					logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": crash error file exists: " + str(os.path.join("/home/chronos/user/crash", file)))
					shutil.copy(os.path.join("/home/chronos/user/crash", file), iterationFolderCompletePath)
					os.remove(os.path.join("/home/chronos/user/crash", file))

		# This location contains console-ramoops file
		if os.path.isdir ("/sys/fs/pstore"):
			for file in os.listdir("/sys/fs/pstore"):
				logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": crash error file exists: " + str(os.path.join("/sys/fs/pstore", file)))
				shutil.copy(os.path.join("/sys/fs/pstore", file), iterationFolderCompletePath)
				os.remove(os.path.join("/sys/fs/pstore", file))

		if os.path.isdir ("/dev/pstore"):
			for file in os.listdir("/dev/pstore"):
				logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": crash error file exists: " + str(os.path.join("/dev/pstore", file)))
				shutil.copy(os.path.join("/dev/pstore", file), iterationFolderCompletePath)
				os.remove(os.path.join("/dev/pstore", file))

		if os.path.exists ("/sys/class/drm/card0/error"):

			# Do not copy if file contains "No error state collected"
			drm_card0_error_String = execute_Command("cat /sys/class/drm/card0/error")

			if "No error state collected" not in drm_card0_error_String:
				logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": crash error file exists: /sys/class/drm/card0/error")
				shutil.copy("/sys/class/drm/card0/error", iterationFolderCompletePath)
			else:
				logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": drm_card0_error_String: " + str(drm_card0_error_String))

		if os.path.exists ("/sys/kernel/debug/cros_ec/panicinfo"):
			logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": crash error file exists: /sys/kernel/debug/cros_ec/panicinfo")
			shutil.copy("/sys/kernel/debug/cros_ec/panicinfo", iterationFolderCompletePath)

	except (OSError, IOError, KeyError) as exception:
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

	# store end time
	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Calling sync")
	execute_Command("sync")
	endTime = time.time()

	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Time taken for function execution: " + str(int(endTime-startTime)))

def take_screenshot(iterationFolderCompletePath):
	"""
	Purpose: To take screenshot of all available CRTC IDs

	Parameters:
	iterationFolderCompletePath: String: indicates iteration folder name. This is complete path

	Returns: None
	"""

	""" Create frame object """
	frameObj = currentframe()

	""" String to track current function name """
	functionName = str(frameObj.f_code.co_name) + "()" # Function name

	# store starting time
	startTime = time.time()

	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Entered")

	if os.path.isdir(iterationFolderCompletePath):
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": directory exists: " + iterationFolderCompletePath)
	else:
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": directory does not exist: " + iterationFolderCompletePath)
		return

	string_i915_display_info_Output = execute_Command("cat /sys/kernel/debug/dri/*/i915_display_info")
	list_i915_display_info_Output = string_i915_display_info_Output.split("\n")

	# Returns a datetime object containing the local date and time
	nowTimeDate = datetime.datetime.now()
	string_NowTimeDate = nowTimeDate.strftime("%d%m%Y_%H%M%S")

	error_Flag_Screenshot = 0

	for index in range(1, len(list_i915_display_info_Output)):
		display_width=0
		display_height=0

		if "active=yes" in list_i915_display_info_Output[index]:

			# Sample line: uapi: enable=yes, active=yes, mode="1920x1280": 60 164740 1920 1944 1992 2080 1280 1286 1303 1320 0x48 0xa
			#if "mode=" in list_i915_display_info_Output[index]:
				#display_width, display_height = (list_i915_display_info_Output[index].split("mode="))[1].split("\"")[1].split("x")
				#display_width = int(display_width)
				#display_height = int (display_height)

			if "CRTC:" in list_i915_display_info_Output[index - 1]:

				line_CRTC_displays = str(list_i915_display_info_Output[index - 1])
				logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": line_CRTC_displays: " + line_CRTC_displays)

				for CRTC_display in line_CRTC_displays.splitlines():

					if "CRTC" in CRTC_display:
						# CRTC:91:pipe A
						CRTC_display_ID = CRTC_display.split(":")[1]
						if(CRTC_display_ID.isnumeric()):
							screenshotFileName=os.path.join(iterationFolderCompletePath, "screenshot_" + CRTC_display_ID + "_" + string_NowTimeDate + ".png")
							logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Before screenshot --crtc-id=" + CRTC_display_ID + " " + screenshotFileName)
							# execute_Command("screenshot --crtc-id=" + CRTC_display_ID + " " + os.path.join(iterationFolderCompletePath, "screenshot_" + CRTC_display_ID + "_" + string_NowTimeDate + ".png"))

							os.system("screenshot --crtc-id=" + CRTC_display_ID + " " + screenshotFileName + " 2>/dev/null")

							# We need to wait for screenshot command to save PNG file
							time.sleep (constants.TIME_TWO_SECONDS)
							logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": After screenshot command: " + screenshotFileName)

							if os.path.isfile (screenshotFileName):
								screenshotFileSize = os.path.getsize(screenshotFileName)
								logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": screenshotFileName: " + screenshotFileName + ", screenshotFileSize: " + str(screenshotFileSize))

								# We reduce the size of image file only if it is more than desired size
								if int(screenshotFileSize) < constants.SCREENSHOT_MINIMUM_SIZE:
									error_Flag_Screenshot = 1
									logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): screenshot is less than expected for CRTC_display_ID: " + CRTC_display_ID)
									append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: ERROR: screenshot is less than expected for CRTC_display_ID: " + CRTC_display_ID + "\n", os.path.join(constants.LOG_DIRECTORY_FULL_PATH, constants.ERROR_DETAILS_FILE))
									retain_log_files(iterationFolderCompletePath)
								else:
									screenshotResizeFileName=os.path.join(iterationFolderCompletePath, "screenshot_" + CRTC_display_ID + "_1280x720_" + string_NowTimeDate + ".png")
									os.system("convert " + screenshotFileName + " -resize 1280x720 " + screenshotResizeFileName + " 2>/dev/null")

									logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": After convert command: " + screenshotResizeFileName)

									try:
										os.remove (screenshotFileName)
									except (OSError, IOError) as exception:
										logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

									logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": After screenshot operations")

							else:
								error_Flag_Screenshot = 1
								logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": screenshotFileName is not generated: " + screenshotFileName)

	# Check if flag is set
	if error_Flag_Screenshot == 1:
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error_Flag_Screenshot == 1")

		try:
			with open(constants.JSON_CONFIG_FILE_TEST_PARAMETERS) as fileObjectConfigTestParameters:
				dataTestParameters = json.load(fileObjectConfigTestParameters)

				# Iterating through the json dict
				for stringParameter in dataTestParameters:

					# Perform case-insensitive comparison
					if (stringParameter.casefold() == "stop_on_error_screenshot".casefold()):
						if (dataTestParameters[stringParameter].casefold() == "yes".casefold()):
							logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": before writing file for stop_on_error")

							try:
								with open(constants.STOP_ON_ERROR_FILE,"w") as fileObjectStopOnError:
									fileObjectStopOnError.write (str("STOP_ON_ERROR"))

							except (OSError, IOError) as exception:
								logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

							logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": after writing files for stop_on_error")

						else:
							logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": stop_on_error for prev_sleep_state is NOT enabled")

		except (OSError, IOError, KeyError, json.decoder.JSONDecodeError) as exception:
			logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

			logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": exiting script")
			exit()
	else:
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error_Flag_Screenshot != 1")

	# store end time
	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Calling sync")
	execute_Command("sync")
	endTime = time.time()

	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Time taken for function execution: " + str(int(endTime-startTime)))

	if int(endTime-startTime) > constants.TIME_FIFTEEN_SECONDS:
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): execution time for " + functionName + " is more than " + str(constants.TIME_FIFTEEN_SECONDS))
		append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: ERROR: execution time for " + functionName + " is more than " + str(constants.TIME_FIFTEEN_SECONDS) + "\n", os.path.join(constants.LOG_DIRECTORY_FULL_PATH, constants.ERROR_DETAILS_FILE))
		retain_log_files(iterationFolderCompletePath)

def write_string_to_file(stringMessage, filePath):
	"""
	Purpose: To write string content into file. If file does not exist, it will create.

	Parameters: 
	stringMessage: string output to write to file
	filePath: String: indicates file name to write to. This is complete file path

	Returns: None
    """

	""" Create frame object """
	frameObj = currentframe()

	""" String to track current function name """
	functionName = str(frameObj.f_code.co_name) + "()" # Function name

	try:
		with open(filePath,"w") as fileObject:
			fileObject.write (str(stringMessage))

	except (OSError, IOError) as exception:
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

def append_String_To_File(stringMessage, filePath):
	"""
	Purpose: To append string content into file. If file does not exist, it will create.

	Parameters: 
	stringMessage: string output to write to file
	filePath: String: indicates file name to write to. This is complete file path

	Returns: None
    """

	""" Create frame object """
	frameObj = currentframe()

	""" String to track current function name """
	functionName = str(frameObj.f_code.co_name) + "()" # Function name

	try:
		with open(filePath,"a") as fileObject:
			fileObject.write (str(stringMessage))

	except (OSError, IOError) as exception:
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

def kill_specific_process(processName):
	"""
	Purpose: kill specific process

	Parameters: 
	processName: String name of process to kill. For example, dmesg, btmon, tcpdump

	Returns: None
    """

	""" Create frame object """
	frameObj = currentframe()

	""" String to track current function name """
	functionName = str(frameObj.f_code.co_name) + "()" # Function name

	# store starting time
	startTime = time.time()

	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Entered: " + processName)

	PROCESS_INSTANCE = execute_Command("ps -C " + processName + " | grep " + processName + " | wc -l")
	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": PROCESS_INSTANCE: " + PROCESS_INSTANCE)

	if (int(PROCESS_INSTANCE) != 0):
		# Kill all dmesg logging process
		execute_Command("pkill -9 " + processName + " &>/dev/null")
		time.sleep (constants.TIME_ONE_SECOND)

		PROCESS_INSTANCE = execute_Command("ps -C " + processName + " | grep " + processName + " | wc -l")
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": PROCESS_INSTANCE: " + PROCESS_INSTANCE)

	# store end time
	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Calling sync")
	execute_Command("sync")
	endTime = time.time()

	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Time taken for function execution: " + str(int(endTime-startTime)))

def measure_filesize_for_original(iterationFolderCompletePath):
	"""
	Purpose: To check file size of files saved in original

	Parameters: 
	iterationFolderCompletePath: String: indicates iteration folder name. This includes complete path

	Returns: None
    """

	""" Create frame object """
	frameObj = currentframe()

	""" String to track current function name """
	functionName = str(frameObj.f_code.co_name) + "()" # Function name

	# store starting time
	startTime = time.time()

	try:
		# Compare file size only in FF devices
		with open(constants.JSON_CONFIG_FILE_TEST_PARAMETERS) as fileObjectConfigTestParameters:
			dataTestParameters = json.load(fileObjectConfigTestParameters)

			# Iterating through the json dict
			for stringParameter in dataTestParameters:
				# Perform case-insensitive comparison
				if (stringParameter.casefold() == "compare_file_sizes_of_original".casefold()):
					if (dataTestParameters[stringParameter].casefold() == "yes".casefold()):
						logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": compare_file_sizes_of_original is enabled")
	
						with open(constants.JSON_CONFIG_FILE_COMPARE_LOGS) as fileObjectConfigCompareLogs:
							dataFileCompareLogs = json.load(fileObjectConfigCompareLogs)

							# Iterating through the json dict
							for originalFileName in dataFileCompareLogs['compare_file_sizes_of_original']:

								if os.path.isfile (os.path.join(constants.LOG_DIRECTORY_FULL_PATH, constants.ORIGINAL_FOLDER_NAME, originalFileName)):
									originalfileObservedSize = os.path.getsize(os.path.join(constants.LOG_DIRECTORY_FULL_PATH, constants.ORIGINAL_FOLDER_NAME, originalFileName))

									originalfileExpectedSize = dataFileCompareLogs['compare_file_sizes_of_original'][originalFileName]

									# Track file size comparison only as non-zero
									if int(originalfileObservedSize) == 0:
										logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): File size of original file is zero for " + originalFileName)
										append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: ERROR: File size of original file is zero for " + originalFileName + "\n", os.path.join(constants.LOG_DIRECTORY_FULL_PATH, constants.ERROR_DETAILS_FILE))
										retain_log_files(iterationFolderCompletePath)
									else:
										if int(originalfileObservedSize) < int(originalfileExpectedSize):
											logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): File size of original file is less than expected size for " + originalFileName)
											append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: ERROR: File size of original file is less than expected size for " + originalFileName + "\n", os.path.join(constants.LOG_DIRECTORY_FULL_PATH, constants.ERROR_DETAILS_FILE))
											retain_log_files(iterationFolderCompletePath)

								else:
									logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": File does not exist in original folder: " + originalFileName)
									# Ideally, we should catch this error. Needs test parameters flags to be tracked
									# Commenting out for now
									# append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: ERROR: File does not exist in original folder: " + originalFileName + "\n", os.path.join(constants.LOG_DIRECTORY_FULL_PATH, constants.ERROR_DETAILS_FILE))

	except (OSError, IOError, KeyError, json.decoder.JSONDecodeError, requests.exceptions.Timeout, requests.exceptions.RequestException) as exception:
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): error: " + str(exception))
		append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: ERROR: measure filesize for original is not initiated\n", os.path.join(constants.LOG_DIRECTORY_FULL_PATH, constants.ERROR_DETAILS_FILE))
		retain_log_files(iterationFolderCompletePath)

	# store end time
	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Calling sync")
	execute_Command("sync")
	endTime = time.time()

	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Time taken for function execution: " + str(int(endTime-startTime)))

def check_retain_status_and_delete_files(iterationFolderCompletePath):
	"""
	Purpose: To stop test execution, if stop_on_error file is present

	Parameters: 
	iterationFolderCompletePath: String: indicates iteration folder name. This includes complete path

	Returns: None
    """

	""" Create frame object """
	frameObj = currentframe()

	""" String to track current function name """
	functionName = str(frameObj.f_code.co_name) + "()" # Function name

	# store starting time
	startTime = time.time()

	# If this file exists, we do not delete content in folder iterationFolderCompletePath
	if os.path.exists (constants.RETAIN_LOG_FILES):

		try:
			logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file exists: " + constants.RETAIN_LOG_FILES)
			os.remove (constants.RETAIN_LOG_FILES)
		except (OSError, IOError) as exception:
			logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

	else:
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file does not exist: " + constants.RETAIN_LOG_FILES)

		try:
			delete_filelist = [f for f in os.listdir(iterationFolderCompletePath) if (not f.endswith("dmesg.txt") and not f.endswith("tcpdump.pcap") and not f.endswith("btmon_snoop.txt") and not f.endswith("cros_ec_original.txt") and not f.endswith(".png") and not f.endswith("package_cstate_show.txt") and not f.endswith("slp_s0_residency_usec.txt") and not f.endswith("typecd.log"))]

			for delete_filename in delete_filelist:
				os.remove(os.path.join(iterationFolderCompletePath, delete_filename))
		except (OSError, IOError) as exception:
			logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

def check_stop_on_error_status():
	"""
	Purpose: To stop test execution, if stop_on_error file is present

	Parameters: None

	Returns: None
    """

	""" Create frame object """
	frameObj = currentframe()

	""" String to track current function name """
	functionName = str(frameObj.f_code.co_name) + "()" # Function name

	# store starting time
	startTime = time.time()

	if os.path.exists (constants.STOP_ON_ERROR_FILE):
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file exists: " + constants.STOP_ON_ERROR_FILE)

		kill_specific_process("dmesg")
		kill_specific_process("btmon")
		kill_specific_process("tcpdump")

		save_error_summary()

		if os.path.exists (constants.CONF_FILE_ETC_INIT):
			try:
				logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file exists: " + constants.CONF_FILE_ETC_INIT)
				os.remove (constants.CONF_FILE_ETC_INIT)
			except (OSError, IOError) as exception:
				logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))
		else:
			logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file does not exist: " + constants.CONF_FILE_ETC_INIT)

		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Before playing /dev/urandom")
		execute_Command("timeout --signal=KILL 3 aplay /dev/urandom")
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": stop_on_error_String is not STOP_ON_ERROR_NO")

		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": exiting script")
		exit()
	else:
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file does not exist: " + constants.STOP_ON_ERROR_FILE)

def enable_Thunderbolt_USB4_enumeration(iterationFolderCompletePath):
	"""
	Purpose: Enable Thunderbolt connection

	Parameters: 
	iterationFolderCompletePath: String: indicates iteration folder name. This includes complete path

	Returns: None
    """

	""" Create frame object """
	frameObj = currentframe()

	""" String to track current function name """
	functionName = str(frameObj.f_code.co_name) + "()" # Function name

	# store starting time
	startTime = time.time()

	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Entered")

	try:
		# Enable below line to enable DRM logging
		with open(constants.JSON_CONFIG_FILE_TEST_PARAMETERS) as fileObjectConfigTestParameters:
			dataTestParameters = json.load(fileObjectConfigTestParameters)

			# Iterating through the json dict
			for stringParameter in dataTestParameters:
				# Perform case-insensitive comparison
				if (stringParameter.casefold() == "enumerate_Thunderbolt_TR_devices".casefold()):
					if (dataTestParameters[stringParameter].casefold() == "yes".casefold()):
						# Needed for TBT TR devices
						# To do: instead of hard-code port, find dynamically
						# To do: need so many sleep commands?
						execute_Command("ectool typeccontrol 0 0")
						execute_Command("ectool typeccontrol 1 0")
						execute_Command("ectool typeccontrol 0 2 1")
						execute_Command("ectool typeccontrol 1 2 1")

						time.sleep(constants.TIME_ONE_SECOND)

						# Generic commands
						execute_Command("echo 0 > /sys/bus/pci/drivers_allowlist_lockdown")

						time.sleep(constants.TIME_ONE_SECOND)

						execute_Command("for THUNDERBOLT_DEVICE in /sys/bus/thunderbolt/devices/*/authorized; do if [ -f $THUNDERBOLT_DEVICE ]; then echo 1 > $THUNDERBOLT_DEVICE; fi; done")

						time.sleep(constants.TIME_ONE_SECOND)

				# Perform case-insensitive comparison
				if (stringParameter.casefold() == "enumerate_TBT_AR_USB4_devices".casefold()):
					if (dataTestParameters[stringParameter].casefold() == "yes".casefold()):
						# Generic commands
						execute_Command("echo 0 > /sys/bus/pci/drivers_allowlist_lockdown")

						time.sleep(constants.TIME_ONE_SECOND)

						execute_Command("for THUNDERBOLT_DEVICE in /sys/bus/thunderbolt/devices/*/authorized; do if [ -f $THUNDERBOLT_DEVICE ]; then echo 1 > $THUNDERBOLT_DEVICE; fi; done")

						time.sleep(constants.TIME_ONE_SECOND)

	except (OSError, IOError, KeyError, json.decoder.JSONDecodeError) as exception:
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": exiting script")
		exit()

	# store end time
	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Calling sync")
	execute_Command("sync")
	endTime = time.time()

	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Time taken for function execution: " + str(int(endTime-startTime)))

def check_Thunderbolt_Connection(iterationFolderCompletePath):
	"""
	Purpose: Check if Thunderbolt connection is correct: Alpine Ridge (AR) or Titan Ridge (TR)

	Parameters: 
	iterationFolderCompletePath: String: indicates iteration folder name. This includes complete path

	Returns: None
    """

	""" Create frame object """
	frameObj = currentframe()

	""" String to track current function name """
	functionName = str(frameObj.f_code.co_name) + "()" # Function name

	# store starting time
	startTime = time.time()

	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Entered")

	string_fileObjectlspciFile = ""
	string_fileObject_ectool_output_File = ""
	error_TBT_AR_TR=0

	try:
		# \\CCGBAFILSVR01\Chrome_Logs_And_Build_Images\Logs\DeviceHealthCheck\Radiohead\ww17\tbtdock\cold boot\1557\2_26042022_120711_cold_boot_s0_s5_g3_detailed
		with open(os.path.join(iterationFolderCompletePath, "lspci_original.txt"), 'r') as fileObjectlspci:
			string_fileObjectlspciFile = fileObjectlspci.read()

		with open(os.path.join(iterationFolderCompletePath, "ectool_output.txt"), 'r') as fileObject_ectool_output:
			string_fileObject_ectool_output_File = fileObject_ectool_output.read()

		# If lspci has any one entry of TBT, usbpdmuxinfo must have TBT=1
		if ( (constants.TBT_TITAN_RIDGE_DEVICE_ID in string_fileObjectlspciFile or constants.TBT_ALPINE_RIDGE_DEVICE_ID in string_fileObjectlspciFile) and ("TBT=1" not in string_fileObject_ectool_output_File) ):
			logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): TBT entry missing in usbpdmuxinfo")
			append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: ERROR: TBT entry missing in usbpdmuxinfo\n", os.path.join(constants.LOG_DIRECTORY_FULL_PATH, constants.ERROR_DETAILS_FILE))
			retain_log_files(iterationFolderCompletePath)
			error_TBT_AR_TR=1

		if (constants.TBT_TITAN_RIDGE_DEVICE_ID in string_fileObjectlspciFile):
			logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): Titan Ridge Thunderbolt device connected")
			append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: INFO: Titan Ridge Thunderbolt device connected\n", os.path.join(constants.LOG_DIRECTORY_FULL_PATH, constants.ERROR_DETAILS_FILE))
			retain_log_files(iterationFolderCompletePath)
			error_TBT_AR_TR=1

		if (constants.TBT_ALPINE_RIDGE_DEVICE_ID in string_fileObjectlspciFile):
			logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): Alpine Ridge Thunderbolt device connected")
			append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: INFO: Alpine Ridge Thunderbolt device connected\n", os.path.join(constants.LOG_DIRECTORY_FULL_PATH, constants.ERROR_DETAILS_FILE))
			retain_log_files(iterationFolderCompletePath)
			error_TBT_AR_TR=1

		if (error_TBT_AR_TR == 1):
			with open(constants.JSON_CONFIG_FILE_TEST_PARAMETERS) as fileObjectConfigTestParameters:
				dataTestParameters = json.load(fileObjectConfigTestParameters)

				# Iterating through the json dict
				for stringParameter in dataTestParameters:

					# Perform case-insensitive comparison
					if (stringParameter.casefold() == "stop_on_error_TBT_AR_TR".casefold()):
						if (dataTestParameters[stringParameter].casefold() == "yes".casefold()):
							logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": before writing file for stop_on_error for: " + stringParameter)

							try:
								with open(constants.STOP_ON_ERROR_FILE,"w") as fileObjectStopOnError:
									fileObjectStopOnError.write (str("STOP_ON_ERROR"))

							except (OSError, IOError) as exception:
								logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

							logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": after writing files for stop_on_error")

						else:
							logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": stop_on_error for wget download is NOT enabled")

	except (OSError, IOError, KeyError, json.decoder.JSONDecodeError) as exception:
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": exiting script")
		exit()

	# store end time
	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Calling sync")
	execute_Command("sync")
	endTime = time.time()

	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Time taken for function execution: " + str(int(endTime-startTime)))

def save_dmesg_logs(iterationFolderCompletePath):
	"""
	Purpose: Save dmesg information from DUT. First it kills all existing instances of dmesg process

	Parameters: 
	iterationFolderCompletePath: String: indicates iteration folder name. This includes complete path

	Returns: None
    """

	""" Create frame object """
	frameObj = currentframe()

	""" String to track current function name """
	functionName = str(frameObj.f_code.co_name) + "()" # Function name

	# store starting time
	startTime = time.time()

	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Entered")

	kill_specific_process("dmesg")
	kill_specific_process("btmon")
	kill_specific_process("tcpdump")

	try:
		# Enable below line to enable DRM logging
		with open(constants.JSON_CONFIG_FILE_TEST_PARAMETERS) as fileObjectConfigTestParameters:
			dataTestParameters = json.load(fileObjectConfigTestParameters)

			# Iterating through the json dict
			for stringParameter in dataTestParameters:
				# Perform case-insensitive comparison
				if (stringParameter.casefold() == "capture_DRM_logs".casefold()):
					if (dataTestParameters[stringParameter].casefold() == "yes".casefold()):
						logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": capture_DRM_logs is enabled")
						execute_Command("echo 0xe > /sys/module/drm/parameters/debug")

					else:
						logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": capture_DRM_logs is NOT enabled")

	except (OSError, IOError, KeyError, json.decoder.JSONDecodeError) as exception:
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": exiting script")
		exit()

	try:
		os.system("dmesg -w --time-format iso > " + os.path.join(iterationFolderCompletePath, "dmesg.txt") + " &")
	except (FileNotFoundError, OSError, IOError, subprocess.CalledProcessError) as exception:
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": exception: " + str(exception))

		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": exiting script")
		exit()

	# wait for some time for dmesg logs to get saved
	time.sleep (constants.TIME_TWO_SECONDS)

	DMESG_INSTANCE = execute_Command("ps -C dmesg | grep dmesg | wc -l")
	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": DMESG_INSTANCE: " + DMESG_INSTANCE)

	if (int(DMESG_INSTANCE) != 0):
		DMESG_INSTANCE = execute_Command("ps -C dmesg | grep dmesg | wc -l")
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": DMESG_INSTANCE: " + DMESG_INSTANCE)

	# store end time
	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Calling sync")
	execute_Command("sync")
	endTime = time.time()

	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Time taken for function execution: " + str(int(endTime-startTime)))

def save_btmon_and_tcp_dump_logs(iterationFolderCompletePath):
	"""
	Purpose: Save btmon and tcp dump information from DUT. First it kills all existing instances of btmon and tcpdump process

	Parameters: 
	iterationFolderCompletePath: String: indicates iteration folder name. This includes complete path

	Returns: None
    """

	""" Create frame object """
	frameObj = currentframe()

	""" String to track current function name """
	functionName = str(frameObj.f_code.co_name) + "()" # Function name

	# store starting time
	startTime = time.time()

	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Entered")

	kill_specific_process("btmon")
	kill_specific_process("tcpdump")

	# btmon -w $DEVICE_HEALTH_CHECK_LOG_DIRECTORY_FULL_PATH/$CURRENT_ITERATION_FOLDER_NAME/btmon_snoop.log &
	try:
		os.system("btmon -w " + os.path.join(iterationFolderCompletePath, "btmon_snoop.txt") + " > /dev/null 2>&1 &")
	except (FileNotFoundError, OSError, IOError, subprocess.CalledProcessError) as exception:
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": exception: " + str(exception))

		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": exiting script")
		exit()

	# wait for some time for btmon logs to get saved
	time.sleep (constants.TIME_TWO_SECONDS)

	BTMON_INSTANCE = execute_Command("ps -C btmon | grep btmon | wc -l")
	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": BTMON_INSTANCE: " + BTMON_INSTANCE)

	if (int(BTMON_INSTANCE) != 0):
		BTMON_INSTANCE = execute_Command("ps -C btmon | grep btmon | wc -l")
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": BTMON_INSTANCE: " + BTMON_INSTANCE)

	# tcpdump -i usbmon1 -w $DEVICE_HEALTH_CHECK_LOG_DIRECTORY_FULL_PATH/$CURRENT_ITERATION_FOLDER_NAME/tcpdump.pcap & 
	try:
		os.system("tcpdump -i usbmon1 -w " + os.path.join(iterationFolderCompletePath, "tcpdump.pcap") + " > /dev/null 2>&1 &")
	except (FileNotFoundError, OSError, IOError, subprocess.CalledProcessError) as exception:
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": exception: " + str(exception))

		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": exiting script")
		exit()

	# wait for some time for tcpdump logs to get saved
	time.sleep (constants.TIME_TWO_SECONDS)

	TCPDUMP_INSTANCE = execute_Command("ps -C tcpdump | grep tcpdump | wc -l")
	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": TCPDUMP_INSTANCE: " + TCPDUMP_INSTANCE)

	if (int(TCPDUMP_INSTANCE) != 0):
		TCPDUMP_INSTANCE = execute_Command("ps -C tcpdump | grep tcpdump | wc -l")
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": TCPDUMP_INSTANCE: " + TCPDUMP_INSTANCE)

	# store end time
	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Calling sync")
	execute_Command("sync")
	endTime = time.time()

	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Time taken for function execution: " + str(int(endTime-startTime)))


def function_create_stop_on_error_wget_download_for_WWAN(iterationFolderCompletePath):
	"""
	Purpose: Save dmesg information from DUT. First it kills all existing instances of dmesg process

	Parameters: 
	iterationFolderCompletePath: String: indicates iteration folder name. This includes complete path

	Returns: None
    """

	""" Create frame object """
	frameObj = currentframe()

	""" String to track current function name """
	functionName = str(frameObj.f_code.co_name) + "()" # Function name

	# store starting time
	startTime = time.time()

	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Entered")

	try:
		with open(constants.JSON_CONFIG_FILE_TEST_PARAMETERS) as fileObjectConfigTestParameters:
			dataTestParameters = json.load(fileObjectConfigTestParameters)

			# Iterating through the json dict
			for stringParameter in dataTestParameters:

				# Perform case-insensitive comparison
				if (stringParameter.casefold() == "stop_on_error_wget_download_for_WWAN".casefold()):
					if (dataTestParameters[stringParameter].casefold() == "yes".casefold()):
						logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": before writing file for stop_on_error for: " + stringParameter)

						try:
							with open(constants.STOP_ON_ERROR_FILE,"w") as fileObjectStopOnError:
								fileObjectStopOnError.write (str("STOP_ON_ERROR"))

						except (OSError, IOError) as exception:
							logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

						logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": after writing files for stop_on_error")

					else:
						logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": stop_on_error for wget download is NOT enabled")

	except (OSError, IOError, KeyError, json.decoder.JSONDecodeError) as exception:
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": exiting script")
		exit()

def perform_wget_download(iterationFolderCompletePath):
	"""
	Purpose: Save detailed information from DUT

	Parameters: 
	iterationFolderCompletePath: String: indicates iteration folder name. This includes complete path

	Returns: None
    """

	""" Create frame object """
	frameObj = currentframe()

	""" String to track current function name """
	functionName = str(frameObj.f_code.co_name) + "()" # Function name

	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Entered")

	if os.path.isdir(iterationFolderCompletePath):
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": directory exists: " + iterationFolderCompletePath)
	else:
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": directory does not exist: " + iterationFolderCompletePath)
		try:
			os.mkdir(iterationFolderCompletePath)
		except (FileNotFoundError,OSError, IOError) as exception:
			logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

			logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": exiting script")
			exit()

	# store starting time
	startTime = time.time()

	retryCount = 0

	while retryCount < constants.WGET_DOWNLOAD_RETRY_ATTEMPTS:
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": retryCount: " + str(retryCount))

		if (retryCount != 0):
			print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": perform_wget_download retryCount: " + str(retryCount))

		try:
			HTTP_response_HTTP_Download = requests.get(constants.WGET_HTTP_URL, timeout=constants.TIME_TWENTY_SECONDS)

			logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": HTTP response: " + str(HTTP_response_HTTP_Download))

			if (str(HTTP_response_HTTP_Download) == "<Response [200]>"):
				destinationFileHTTPDownload = os.path.join(iterationFolderCompletePath, "music.mp3")
				logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": destination file for HTTP download: " + destinationFileHTTPDownload)

				with open(destinationFileHTTPDownload,'wb') as fileObjectHTTPDownloadedFile:
					# Saving received content as a png file in binary format.
					# write the contents of the response (r.content) to a new file in binary mode.
					numCharsWritten = fileObjectHTTPDownloadedFile.write(HTTP_response_HTTP_Download.content)
					logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": numCharsWritten: " + str(numCharsWritten))
					time.sleep(constants.TIME_ONE_SECOND)

				if (os.path.isfile(destinationFileHTTPDownload)):
					logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": destinationFileHTTPDownload file exists: " + destinationFileHTTPDownload)

					fileSize_HTTP_Download = os.path.getsize(destinationFileHTTPDownload)
					logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file size for HTTP download: " + str(fileSize_HTTP_Download))

					if (fileSize_HTTP_Download != constants.WGET_DOWNLOAD_FILESIZE):
						logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file size for HTTP download is not correct for retry count " + str(retryCount))

						# Print the error only once, when retry count is completed
						if (retryCount == (constants.WGET_DOWNLOAD_RETRY_ATTEMPTS - 1)):
							logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): file size for HTTP download is not correct for retry count: " + str(retryCount))
							append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: ERROR: file size for HTTP download is not correct for retry count " + str(retryCount) + "\n", os.path.join(constants.LOG_DIRECTORY_FULL_PATH, constants.ERROR_DETAILS_FILE))
							retain_log_files(iterationFolderCompletePath)

						logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Before function_create_stop_on_error_wget_download_for_WWAN for retry count " + str(retryCount))
						
						function_create_stop_on_error_wget_download_for_WWAN(iterationFolderCompletePath)

						logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Before ping google")
						ping_Output_String = execute_Command("ping google.com -c 1")
						logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": After Ping google: response: " + str(ping_Output_String))

						ping_Output_String = execute_Command("ping 8.8.8.8 -c 1")
						logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": After Ping 8.8.8.8: response: " + str(ping_Output_String))
					else:
						logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file size for HTTP download is same as expected for retry count " + str(retryCount))
						os.remove (destinationFileHTTPDownload)
						logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": After removing " + destinationFileHTTPDownload)

						# Come out of while loop of retries
						break
				else:
					logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": destinationFileHTTPDownload file does not exists for retry count " + str(retryCount) + " for destinationFileHTTPDownload: " + destinationFileHTTPDownload)

		except (OSError, IOError, KeyError, json.decoder.JSONDecodeError, requests.exceptions.HTTPError, requests.exceptions.Timeout, requests.exceptions.RequestException) as exception:
			logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

			# Print the error only once, when retry count is completed
			if (retryCount == (constants.WGET_DOWNLOAD_RETRY_ATTEMPTS - 1)):
				logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): HTTP download is not initiated for retry count " + str(retryCount))
				append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: ERROR: HTTP download is not initiated for retry count " + str(retryCount) + "\n", os.path.join(constants.LOG_DIRECTORY_FULL_PATH, constants.ERROR_DETAILS_FILE))
				retain_log_files(iterationFolderCompletePath)

			function_create_stop_on_error_wget_download_for_WWAN(iterationFolderCompletePath)

			logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Before ping")
			ping_Output_String = execute_Command("ping google.com -c 1")
			logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": After Ping: response: " + str(ping_Output_String))

		retryCount = retryCount + 1
		
		# Give some delay before we repeat iteration
		time.sleep(constants.TIME_FIVE_SECONDS)

	# store end time
	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Calling sync")
	execute_Command("sync")
	endTime = time.time()

	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Time taken for function execution: " + str(int(endTime-startTime)))

def compare_prev_sleep_state(expected_prev_sleep_state, iterationFolderCompletePath):
	"""
	Purpose: Compare prev_sleep_state with expected value

	Parameters: 
	expected_prev_sleep_state: String: indicates expected prev_sleep_state value

	Returns: None
    """

	""" Create frame object """
	frameObj = currentframe()

	""" String to track current function name """
	functionName = str(frameObj.f_code.co_name) + "()" # Function name

	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Entered")

	if (expected_prev_sleep_state != constants.PREV_SLEEP_STATE_WARM_BOOT) and (expected_prev_sleep_state != constants.PREV_SLEEP_STATE_COLD_BOOT):
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": ERROR: expected prev_sleep_state passed to function is not 0 or 5: " + expected_prev_sleep_state)

		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": exiting script")
		exit()

	# store starting time
	startTime = time.time()

	try:
		# Cold boot: prev_sleep_state 5
		# Warm boot: prev_sleep_state 0
		observed_prev_sleep_state=execute_Command(constants.CBMEM_1_PREV_SLEEP_STATE).strip()

		if (((constants.PREV_SLEEP_STATE_WARM_BOOT in expected_prev_sleep_state) and (constants.PREV_SLEEP_STATE_WARM_BOOT in observed_prev_sleep_state)) or ((constants.PREV_SLEEP_STATE_COLD_BOOT in expected_prev_sleep_state) and (constants.PREV_SLEEP_STATE_COLD_BOOT in observed_prev_sleep_state))):
			logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": prev_sleep_state is as expected: " + observed_prev_sleep_state)
		else:
			logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno)  + ":\t" + iterationFolderCompletePath + "\t: ERROR: prev_sleep_state is not as expected: " + observed_prev_sleep_state)

			with open(constants.JSON_CONFIG_FILE_TEST_PARAMETERS) as fileObjectConfigTestParameters:
				dataTestParameters = json.load(fileObjectConfigTestParameters)

				# Iterating through the json dict
				for stringParameter in dataTestParameters:

					# Perform case-insensitive comparison
					if (stringParameter.casefold() == "stop_on_error_prev_sleep_state".casefold()):
						if (dataTestParameters[stringParameter].casefold() == "yes".casefold()):
							logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": before writing file for stop_on_error")

							try:
								with open(constants.STOP_ON_ERROR_FILE,"w") as fileObjectStopOnError:
									fileObjectStopOnError.write (str("STOP_ON_ERROR"))

							except (OSError, IOError) as exception:
								logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

							logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": after writing files for stop_on_error")

						else:
							logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": stop_on_error for prev_sleep_state is NOT enabled")

	except (OSError, IOError, KeyError, json.decoder.JSONDecodeError) as exception:
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": exiting script")
		exit()

	# store end time
	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Calling sync")
	execute_Command("sync")
	endTime = time.time()

	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Time taken for function execution: " + str(int(endTime-startTime)))

def save_detailed_logs(iterationFolderCompletePath):
	"""
	Purpose: Save detailed information from DUT

	Parameters: 
	iterationFolderCompletePath: String: indicates iteration folder name. This includes complete path

	Returns: None
    """

	""" Create frame object """
	frameObj = currentframe()

	""" String to track current function name """
	functionName = str(frameObj.f_code.co_name) + "()" # Function name

	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Entered")

	if os.path.isdir(iterationFolderCompletePath):
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": directory exists: " + iterationFolderCompletePath)
	else:
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": directory does not exist: " + iterationFolderCompletePath)
		try:
			os.mkdir(iterationFolderCompletePath)
		except (FileNotFoundError,OSError, IOError) as exception:
			logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

			logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": exiting script")
			exit()

	if os.path.isfile(constants.JSON_CONFIG_FILE_SAVE_DETAILED_LOGS):
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file exists: " + constants.JSON_CONFIG_FILE_SAVE_DETAILED_LOGS)
	else:
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file does not exist: " + constants.JSON_CONFIG_FILE_SAVE_DETAILED_LOGS)
		return

	save_dmesg_logs(iterationFolderCompletePath)

	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": before login_to_DUT()")

	login_to_DUT(iterationFolderCompletePath)

	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": after login_to_DUT()")

	# Set corp proxy
	set_corp_proxy(iterationFolderCompletePath)

	# store starting time
	startTime = time.time()

	""" One time commands before tests start """
	execute_Command("amixer set Master 50%")

	# Enable TBT devices enumeration
	enable_Thunderbolt_USB4_enumeration(iterationFolderCompletePath)

	# Save BTMon and tcpdump logs
	# save_btmon_and_tcp_dump_logs(iterationFolderCompletePath)

	if os.path.isdir(constants.LOGIN_HOME_DIRECTORY):
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": DUT is logged in")
	else:
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": DUT is logged out")

	try:
		with open(constants.JSON_CONFIG_FILE_SAVE_DETAILED_LOGS) as fileObjectSaveDetailedLogs:
			dataSaveDetailedLogs = json.load(fileObjectSaveDetailedLogs)

			with open(constants.JSON_CONFIG_FILE_TEST_PARAMETERS) as fileObjectConfigTestParameters:
				dataTestParameters = json.load(fileObjectConfigTestParameters)

				count_Save_Files = 0

				# Dump this only in original
				# Iterating through the json dict
				if (constants.ORIGINAL_FOLDER_NAME in iterationFolderCompletePath):
					logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": dumping original")

					for commandString in dataSaveDetailedLogs['save_detailed_logs_Only_in_original']:
						outputString = execute_Command(commandString)

						# Check if string returned in empty
						if outputString is None or len(outputString) == 0:
							outputString = "\n"

						append_String_To_File(outputString, os.path.join(iterationFolderCompletePath, dataSaveDetailedLogs['save_detailed_logs_Only_in_original'][commandString]))
						count_Save_Files = count_Save_Files + 1
				else:
					logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": NOT dumping original")

				# Iterating through the json dict
				for commandString in dataSaveDetailedLogs['save_detailed_logs_RVP_and_FF']:
					outputString = execute_Command(commandString)

					# Check if string returned in empty
					if outputString is None or len(outputString) == 0:
						outputString = "\n"

					append_String_To_File(outputString, os.path.join(iterationFolderCompletePath, dataSaveDetailedLogs['save_detailed_logs_RVP_and_FF'][commandString]))
					count_Save_Files = count_Save_Files + 1

				# Iterating through the json dict
				for stringParameter in dataTestParameters:
					# Perform case-insensitive comparison
					if (stringParameter.casefold() == "collect_ADL_specific_logs".casefold()):
						if (dataTestParameters[stringParameter].casefold() == "yes".casefold()):
							logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": collect_ADL_specific_logs is enabled. Before reading logs")

							# Iterating through the json dict
							for commandString in dataSaveDetailedLogs['collect_ADL_specific_logs']:
								outputString = execute_Command(commandString)

								# Check if string returned in empty
								if outputString is None or len(outputString) == 0:
									outputString = "\n"

								append_String_To_File(outputString, os.path.join(iterationFolderCompletePath, dataSaveDetailedLogs['collect_ADL_specific_logs'][commandString]))
								count_Save_Files = count_Save_Files + 1
						
							logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": collect_ADL_specific_logs is enabled. After reading logs")

						else:
							logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": collect_ADL_specific_logs is NOT enabled")

					# Perform case-insensitive comparison
					if (stringParameter.casefold() == "save_detailed_logs_only_On_FF".casefold()):
						if (dataTestParameters[stringParameter].casefold() == "yes".casefold()):
							logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": save_detailed_logs_only_On_FF is enabled")

							# Iterating through the json dict
							for commandString in dataSaveDetailedLogs['save_detailed_logs_only_On_FF']:
								outputString = execute_Command(commandString)

								# Check if string returned in empty
								if outputString is None or len(outputString) == 0:
									outputString = "\n"

								append_String_To_File(outputString, os.path.join(iterationFolderCompletePath, dataSaveDetailedLogs['save_detailed_logs_only_On_FF'][commandString]))
								count_Save_Files = count_Save_Files + 1

						else:
							logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": save_detailed_logs_only_On_FF is NOT enabled")

					# Perform case-insensitive comparison
					if (stringParameter.casefold() == "save_detailed_logs_for_WWAN".casefold()):
						if (dataTestParameters[stringParameter].casefold() == "yes".casefold()):
							logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": save_detailed_logs_for_WWAN is enabled")

							# Iterating through the json dict
							for commandString in dataSaveDetailedLogs['save_detailed_logs_for_WWAN']:
								outputString = execute_Command(commandString)

								# Check if string returned in empty
								if outputString is None or len(outputString) == 0:
									outputString = "\n"

								append_String_To_File(outputString, os.path.join(iterationFolderCompletePath, dataSaveDetailedLogs['save_detailed_logs_for_WWAN'][commandString]))
								count_Save_Files = count_Save_Files + 1

						else:
							logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": save_detailed_logs_for_WWAN is NOT enabled")


					# Perform case-insensitive comparison
					if (stringParameter.casefold() == "perform_wget_download_for_WWAN".casefold()):
						if(dataTestParameters[stringParameter].casefold() == "yes".casefold()):
							logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": collect_ADL_specific_logs is enabled")

							# Call function to perform wget download
							perform_wget_download(iterationFolderCompletePath)

							logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": after perform_wget_download()")

							count_Save_Files = count_Save_Files + 1


		# Log this only if # of log files saved is less than 100 (rough estimation)
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Total commands executed to save operation: " + str(count_Save_Files))
		if count_Save_Files < 100:
			logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): Total commands executed for save operation: " + str(count_Save_Files))
			append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: ERROR: Total commands executed for save operation: " + str(count_Save_Files) + "\n", os.path.join(constants.LOG_DIRECTORY_FULL_PATH, constants.ERROR_DETAILS_FILE))
			retain_log_files(iterationFolderCompletePath)

		check_Thunderbolt_Connection(iterationFolderCompletePath)

	except (OSError, IOError, KeyError, json.decoder.JSONDecodeError) as exception:
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": exiting script")
		exit()

	# Copying autotest logs at end, so that it does not mix count of platform logs, and this allows some delay
	if not os.path.isdir(constants.LOGIN_HOME_DIRECTORY):
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": copying autotest logs since directory is not present: " + str(constants.LOGIN_HOME_DIRECTORY))

		try:
			# Iterating through the json file. it is dict of dict
			with open(constants.JSON_CONFIG_FILE_COPY_DUT_FILES) as fileObjectJSONCopyFiles:
				dataCopyDUTFiles = json.load(fileObjectJSONCopyFiles)

				iterationFolderNameWithAutotestCompletePath = os.path.join(iterationFolderCompletePath, "autotest_logs")
				os.mkdir(iterationFolderNameWithAutotestCompletePath)
				logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": iterationFolderNameWithAutotestCompletePath: " + iterationFolderNameWithAutotestCompletePath)

				# Iterating through the json dict
				for autotest_path_file in dataCopyDUTFiles['copy_autotest_logs_on_login_error']:
					if os.path.isfile(autotest_path_file):
						shutil.copy(autotest_path_file, iterationFolderNameWithAutotestCompletePath)
						logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": after writing autotest_path_file: " + autotest_path_file)

		except (FileNotFoundError, OSError, IOError, KeyError, json.decoder.JSONDecodeError) as exception:
			logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": exception: " + str(exception))

			logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": exiting script")
			exit()

	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling parse_JSON_save_count_values()")
	parse_JSON_save_count_values (iterationFolderCompletePath)

	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling take_screenshot()")
	take_screenshot(iterationFolderCompletePath)

	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Before calling copy_file_to_iteration_folder()")

	copy_file_to_iteration_folder (iterationFolderCompletePath)

	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": After calling copy_file_to_iteration_folder()")

	# store end time
	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Calling sync")
	execute_Command("sync")
	endTime = time.time()

	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Time taken for function execution: " + str(int(endTime-startTime)))

	if int(endTime-startTime) > constants.TIME_FORTY_SECONDS:
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): execution time for " + functionName + " is more than " + str(constants.TIME_FORTY_SECONDS))
		append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno)  + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: ERROR: execution time for " + functionName + " is more than " + str(constants.TIME_FORTY_SECONDS) + "\n", os.path.join(constants.LOG_DIRECTORY_FULL_PATH, constants.ERROR_DETAILS_FILE))
		retain_log_files(iterationFolderCompletePath)

def check_modem_state_at_end_of_testing():
	"""
	Purpose: Check modem state in log file modem_mmcli_m_original.txt

	Parameters: None

	Returns: None
    """

	""" Create frame object """
	frameObj = currentframe()

	""" String to track current function name """
	functionName = str(frameObj.f_code.co_name) + "()" # Function name

	# store starting time
	startTime = time.time()

	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Entered")

	if os.path.isdir(constants.LOG_DIRECTORY_FULL_PATH):
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": directory exist: " + constants.LOG_DIRECTORY_FULL_PATH)
	else:
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": directory does not exist: " + constants.LOG_DIRECTORY_FULL_PATH)
		return

	logFileName = "modem_mmcli_m_dynamic_original.txt"
	try:
		for root,dirs,files in os.walk(constants.LOG_DIRECTORY_FULL_PATH):
			for file in files:
				if (logFileName in file):
					# Create string instance to store complete log file name and path
					logFileNameWithCompletePath = str(os.path.join(root, file))
					logFileNameParentPath = os.path.abspath(os.path.join(logFileNameWithCompletePath, '..'))

					# Adding encoding details, since we get UnicodeDecodeError: ascii codec cant decode byte 0xc0
					fileObjectLog = open(logFileNameWithCompletePath, 'r', encoding='iso-8859-15')
					list_logLines = fileObjectLog.readlines()

					string_SIM_slot_number = ""
					string_modem_state = ""
					string_modem_failed_reason = ""

					for logLine in list_logLines:
						# Search desired string in line
						# |         sim slot paths: slot 1: /org/freedesktop/ModemManager1/SIM/0 (active)
						# |             state: [31mfailed[0m
						# |             state: [32mconnected[0m
						# |             state: searching
						# |     failed reason: [31msim-missing[0m

						if (" slot 1" in logLine and "active" in logLine):
							string_SIM_slot_number = "SIM-slot-1"

						if (" slot 2" in logLine and "active" in logLine):
							string_SIM_slot_number = "SIM-slot-2"

						if ("|     failed reason:" in logLine and "sim-missing" in logLine):
							string_modem_failed_reason = "sim-missing"

						if ("|                  state:" in logLine and "connected" in logLine):
							string_modem_state = "connected"

						if ("|                  state:" in logLine and "Enabled" in logLine):
							string_modem_state = "Enabled"

						if ("|                  state:" in logLine and "failed" in logLine):
							string_modem_state = "failed"

						if ("|                  state:" in logLine and "Registered" in logLine):
							string_modem_state = "Registered"

						if ("|                  state:" in logLine and "searching" in logLine):
							string_modem_state = "searching"

						if ("|                  state:" in logLine and "SIM missing" in logLine):
							string_modem_state = "SIM missing"

					# Print summary at end of reading log file
					# logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": FOR PCT TRACKING: INFO: " + string_SIM_slot_number + " : " + string_modem_state + " " + string_modem_failed_reason)
					logger.info (logFileNameParentPath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): string_SIM_slot_number: " + string_SIM_slot_number + " : " + string_modem_state + " " + string_modem_failed_reason)
					append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ":\t" + logFileNameWithCompletePath + "\t: FOR PCT TRACKING: INFO: " + string_SIM_slot_number + " : " + string_modem_state + " " + string_modem_failed_reason + "\n", os.path.join(constants.LOG_DIRECTORY_FULL_PATH, constants.ERROR_DETAILS_FILE))
					# retain_log_files(logFileNameParentPath)

	except (OSError, IOError, KeyError, json.decoder.JSONDecodeError) as exception:
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": exiting script")
		exit()

	# store end time
	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Calling sync")
	execute_Command("sync")
	endTime = time.time()

	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Time taken for function execution: " + str(int(endTime-startTime)))

def check_errors_during_iteration(iterationFolderCompletePath, Error_String_file_Purpose):
	"""
	Purpose: Check if file contains errors

	Parameters:
	iterationFolderCompletePath: String: indicates iteration's folder which contains desired log file. This includes complete path, without file name
	
	Error_String_file_Purpose: It indicates log file name to search for. It will one of dmesg, console-ramoops typecd or EC log files

	Returns: None
    """

	""" Create frame object """
	frameObj = currentframe()

	""" String to track current function name """
	functionName = str(frameObj.f_code.co_name) + "()" # Function name

	# store starting time
	startTime = time.time()

	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": iterationFolderCompletePath: " + iterationFolderCompletePath)
	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Error_String_file_Purpose: " + Error_String_file_Purpose)

	if ((Error_String_file_Purpose != constants.ERROR_STRING_CONSOLERAMOOPS) and (Error_String_file_Purpose != constants.ERROR_STRING_DMESG) and (Error_String_file_Purpose != constants.ERROR_STRING_EC) and (Error_String_file_Purpose != constants.ERROR_STRING_MMCLI) and (Error_String_file_Purpose != constants.ERROR_STRING_TYPECD)):
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": string is not appropriate")
		return

	logFilename = ""
	JSON_String_Name = ''

	if (Error_String_file_Purpose == constants.ERROR_STRING_CONSOLERAMOOPS):
		logFilename = "console-ramoops-0"
		JSON_String_Name = 'console_ram_oops_error_string'

	if (Error_String_file_Purpose == constants.ERROR_STRING_DMESG):
		logFilename = "dmesg.txt"
		JSON_String_Name = 'dmesg_kernel_error_string'

	if (Error_String_file_Purpose == constants.ERROR_STRING_EC):
		logFilename = "cros_ec_original.txt"
		JSON_String_Name = 'ec_error_string'

	if (Error_String_file_Purpose == constants.ERROR_STRING_MMCLI):
		logFilename = "modem_mmcli_L_original.txt"
		JSON_String_Name = 'modem_mmcli_error_string'

	if (Error_String_file_Purpose == constants.ERROR_STRING_TYPECD):
		logFilename = "typecd.log"
		JSON_String_Name = 'typecd_error_string'

	desiredLogFileNameWithCompletePath = os.path.join(iterationFolderCompletePath, logFilename)

	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": desiredLogFileNameWithCompletePath: " + desiredLogFileNameWithCompletePath)

	if os.path.isfile(desiredLogFileNameWithCompletePath):
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file exists: " + desiredLogFileNameWithCompletePath)
	else:
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file does not exists: " + desiredLogFileNameWithCompletePath)
		return

	if os.path.isfile(constants.JSON_CONFIG_FILE_ERROR_STRINGS):
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file exists: " + constants.JSON_CONFIG_FILE_ERROR_STRINGS)
	else:
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file does not exist: " + constants.JSON_CONFIG_FILE_ERROR_STRINGS)
		return

	try:
		with open(desiredLogFileNameWithCompletePath, 'r') as fileObjectLog:
			list_logFile = fileObjectLog.readlines()

		# Iterating through the json file. it is dict of dict
		with open(constants.JSON_CONFIG_FILE_ERROR_STRINGS) as fileObjectECError:
			dataErrorStrings = json.load(fileObjectECError)

			with open(constants.ERROR_DETAILS_FILE, "a") as fileObjectErrorDetails:

				count_logFile_Error_String_Searched = 0

				# Iterating through the json file. It is dict
				for stringLogFileError in dataErrorStrings[JSON_String_Name]:
					stop_on_error_String = dataErrorStrings[JSON_String_Name][stringLogFileError]

					count_logFile_Error_String_Searched = count_logFile_Error_String_Searched + 1

					for (lineIndex, logLine) in enumerate(list_logFile, start=0):

						# Search case-insensitive
						if (stringLogFileError.casefold() in logLine.casefold()):
							logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": stringLogFileError: " + stringLogFileError)

							try:
								list_LogFile_Error_Found = list_logFile[lineIndex-5:lineIndex+5]

								# Check if list is empty, then take from index -> index + 5
								if not list_LogFile_Error_Found:
									list_LogFile_Error_Found = list_logFile[lineIndex:lineIndex+5]

								# Check if list is empty, then take from index -5 -> index
								if not list_LogFile_Error_Found:
									list_LogFile_Error_Found = list_logFile[lineIndex-5:lineIndex]

								# Check if list is empty, then take from index only
								if not list_LogFile_Error_Found:
									list_LogFile_Error_Found = list_logFile[lineIndex]

								fileObjectErrorDetails.write(logFilename + " error message observed during testing: " + stringLogFileError + ": Filepath: " + desiredLogFileNameWithCompletePath + "\n")
								fileObjectErrorDetails.write(str('\n'.join(map(str, list_LogFile_Error_Found))))

								logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": stringLogFileError: " + stringLogFileError)
								logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": stop_on_error_String is: " + stop_on_error_String)

								append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: ERROR: " + logFilename + " : " + stringLogFileError + "\n", os.path.join(constants.LOG_DIRECTORY_FULL_PATH, constants.ERROR_DETAILS_FILE))

								if (stop_on_error_String != "STOP_ON_ERROR_NO"):
									logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": before writing file for stop_on_error for: " + stringLogFileError)

									try:
										with open(constants.STOP_ON_ERROR_FILE,"w") as fileObjectStopOnError:
											fileObjectStopOnError.write (str("STOP_ON_ERROR"))

									except (OSError, IOError) as exception:
										logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

									logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": after writing files for stop_on_error")

							except (ValueError) as exception:
								logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

							# Check the same error only once in a file
							break

		# Log this only if # of errors is less than 2 (rough estimation), to avoid too many prints
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Total error strings compared: " + str(count_logFile_Error_String_Searched))

	except (OSError, IOError, KeyError, json.decoder.JSONDecodeError) as exception:
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": exiting script")
		exit()

	# store end time
	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Calling sync")
	execute_Command("sync")
	endTime = time.time()

	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Time taken for function execution: " + str(int(endTime-startTime)))

def check_errors_at_end_of_testing(Error_String_file_Purpose):
	"""
	Purpose: Check if log file contains errors in complete log directory

	Parameters: Error_String_file_Purpose: It indicates log file name to search for. It will one of dmesg, console-ramoops typecd or EC log files

	Returns: None
    """

	""" Create frame object """
	frameObj = currentframe()

	""" String to track current function name """
	functionName = str(frameObj.f_code.co_name) + "()" # Function name

	# store starting time
	startTime = time.time()

	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Error_String_file_Purpose: " + Error_String_file_Purpose)

	if os.path.isdir(constants.LOG_DIRECTORY_FULL_PATH):
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": directory exist: " + constants.LOG_DIRECTORY_FULL_PATH)
	else:
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": directory does not exist: " + constants.LOG_DIRECTORY_FULL_PATH)
		return

	if os.path.isfile(constants.JSON_CONFIG_FILE_ERROR_STRINGS):
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file exists: " + constants.JSON_CONFIG_FILE_ERROR_STRINGS)
	else:
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file does not exist: " + constants.JSON_CONFIG_FILE_ERROR_STRINGS)
		return

	if ((Error_String_file_Purpose != constants.ERROR_STRING_CONSOLERAMOOPS) and (Error_String_file_Purpose != constants.ERROR_STRING_DMESG) and (Error_String_file_Purpose != constants.ERROR_STRING_EC) and (Error_String_file_Purpose != constants.ERROR_STRING_MMCLI) and (Error_String_file_Purpose != constants.ERROR_STRING_TYPECD)):
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": string is not appropriate")
		return

	logFilename = ""
	JSON_String_Name = ''

	if (Error_String_file_Purpose == constants.ERROR_STRING_CONSOLERAMOOPS):
		logFilename = "console-ramoops-0"
		JSON_String_Name = 'console_ram_oops_error_string'

	if (Error_String_file_Purpose == constants.ERROR_STRING_EC):
		logFilename = "cros_ec_original.txt"
		JSON_String_Name = 'ec_error_string'

	if (Error_String_file_Purpose == constants.ERROR_STRING_DMESG):
		logFilename = "dmesg.txt"
		JSON_String_Name = 'dmesg_kernel_error_string'

	if (Error_String_file_Purpose == constants.ERROR_STRING_MMCLI):
		logFilename = "modem_mmcli_L_original.txt"
		JSON_String_Name = 'modem_mmcli_error_string'

	if (Error_String_file_Purpose == constants.ERROR_STRING_TYPECD):
		logFilename = "typecd.log"
		JSON_String_Name = 'typecd_error_string'

	try:
		with open(constants.ERROR_DETAILS_FILE, "a") as fileObjectErrorDetails:

			# Iterating through the json file. it is dict of dict
			with open(constants.JSON_CONFIG_FILE_ERROR_STRINGS) as fileObjectlogFileError:
				dataErrorStrings = json.load(fileObjectlogFileError)

				for root,dirs,files in os.walk(constants.LOG_DIRECTORY_FULL_PATH):
					for file in files:
						if (logFilename in file):
							# Create string instance to store complete log file name and path
							logFileNameWithCompletePath = str(os.path.join(root, file))
							logFileNameParentPath = os.path.abspath(os.path.join(logFileNameWithCompletePath, '..'))

							# Adding encoding details, since we get UnicodeDecodeError: ascii codec cant decode byte 0xc0
							#fileObjectLog = open(logFileNameWithCompletePath, 'r', encoding='iso-8859-15')
							#logLines = fileObjectLog.read()
							# Iterating through the json file. It is dict
							#for stringLogFileError in dataErrorStrings[JSON_String_Name]:
							#	# stop_on_error_String = dataErrorStrings[JSON_String_Name][stringLogFileError]
							#	# Search error string in files
							#	if (stringLogFileError in logLines):
							#		append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ":\t" + logFileNameParentPath + "\t: FOR PCT TRACKING: ERROR: " + logFilename + ": " + stringLogFileError + "\n", os.path.join(constants.LOG_DIRECTORY_FULL_PATH, constants.ERROR_DETAILS_FILE))

							with open(logFileNameWithCompletePath, 'r') as fileObjectLog:
								list_logFile = fileObjectLog.readlines()

							# Iterating through the json file. It is dict
							for stringLogFileError in dataErrorStrings[JSON_String_Name]:
								for (lineIndex, logLine) in enumerate(list_logFile, start=0):

									# Search case-insensitive
									if (stringLogFileError.casefold() in logLine.casefold()):
										logger.info (logFileNameWithCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": stringLogFileError: " + stringLogFileError)

										try:
											list_LogFile_Error_Found = list_logFile[lineIndex-5:lineIndex+5]

											# Check if list is empty, then take from index -> index + 5
											if not list_LogFile_Error_Found:
												list_LogFile_Error_Found = list_logFile[lineIndex:lineIndex+5]

											# Check if list is empty, then take from index -5 -> index
											if not list_LogFile_Error_Found:
												list_LogFile_Error_Found = list_logFile[lineIndex-5:lineIndex]

											# Check if list is empty, then take from index only
											if not list_LogFile_Error_Found:
												list_LogFile_Error_Found = list_logFile[lineIndex]

											fileObjectErrorDetails.write(logFilename + " error message observed at end of testing: " + stringLogFileError + ": Filepath: " + logFileNameWithCompletePath + "\n")
											fileObjectErrorDetails.write(str('\n'.join(map(str, list_LogFile_Error_Found))))

											logger.info (logFileNameWithCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": stringLogFileError: " + stringLogFileError)

										except (ValueError) as exception:
											logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

										# Check the same error only once in a file
										break


	except (OSError, IOError, KeyError, json.decoder.JSONDecodeError) as exception:
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": exiting script")
		exit()

	# store end time
	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Calling sync")
	execute_Command("sync")
	endTime = time.time()

	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Time taken for function execution: " + str(int(endTime-startTime)))

def compare_logs(originalFolderWithCompletePath, iterationFolderCompletePath):
	"""
	Purpose: Compare files in original folder and iteration folder

	Parameters: 
	originalFolderWithCompletePath: String: indicates original folder which contains log files. This includes complete path
	iterationFolderCompletePath: String: indicates iteration's folder which contains log files. This includes complete path

	Returns: None
    """

	""" Create frame object """
	frameObj = currentframe()

	""" String to track current function name """
	functionName = str(frameObj.f_code.co_name) + "()" # Function name

	# store starting time
	startTime = time.time()

	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Entered")

	if os.path.isdir(originalFolderWithCompletePath):
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": directory exists: " + originalFolderWithCompletePath)
	else:
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": directory does not exist: " + originalFolderWithCompletePath)
		return

	if os.path.isdir(iterationFolderCompletePath):
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": directory exists: " + iterationFolderCompletePath)
	else:
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": directory does not exist: " + iterationFolderCompletePath)
		return

	# Case-insensitive comparison to ensure original and iteration folder name are not same by mistake
	if (originalFolderWithCompletePath.casefold() != iterationFolderCompletePath.casefold()):
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": original and iteration folder are NOT same")
	else:
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": original and iteration folder are same")
		return

	if os.path.isfile(constants.JSON_CONFIG_FILE_COMPARE_LOGS):
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file exists: " + constants.JSON_CONFIG_FILE_COMPARE_LOGS)
	else:
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file does not exist: " + constants.JSON_CONFIG_FILE_COMPARE_LOGS)
		return

	try:
		# Iterating through the json file. it is dict of dict
		with open(constants.JSON_CONFIG_FILE_COMPARE_LOGS) as fileObjectJSONCompare:
			dataCompareLogs = json.load(fileObjectJSONCompare)
			count_compare_Files = 0

			# Iterating through the json file. It is dict of dict	
			for comparisonFileName in dataCompareLogs['compare_iteration_with_original']:
				stop_on_error_String = dataCompareLogs['compare_iteration_with_original'][comparisonFileName]

				if os.path.isfile(os.path.join(originalFolderWithCompletePath, comparisonFileName)):

					if os.path.isfile(os.path.join(iterationFolderCompletePath, comparisonFileName)):

						with open(os.path.join(originalFolderWithCompletePath, comparisonFileName), 'r') as hosts0:
							with open(os.path.join(iterationFolderCompletePath, comparisonFileName), 'r') as hosts1:
								count_compare_Files = count_compare_Files + 1

								# Do not give full name of original file name, we will create summary out of this file
								diff = difflib.unified_diff(
									hosts0.readlines(),
									hosts1.readlines(),
									fromfile=(constants.ORIGINAL_FOLDER_NAME),
									tofile=(iterationFolderCompletePath + "/" + comparisonFileName),
								)

								# TO DO: optimize this logic, what if delta is too much
								list_diff_files = list(diff)

								if len(list_diff_files) > 0:
									logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": len(list_diff_files) is non-zero: " + str(len(list_diff_files)))

									# Re-take screenshot if delta is display related
									if "i915" in comparisonFileName:
										logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": before recapturing screenshot in take_screenshot()")
										take_screenshot(iterationFolderCompletePath)

										logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": after recapturing screenshot in take_screenshot()")
									else:
										logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": i915 NOT in comparisonFileName: " + comparisonFileName)

									# re-capture the logs if any delta occurs
									try:
										with open(constants.JSON_CONFIG_FILE_SAVE_DETAILED_LOGS) as fileObjectConfigSaveDetailedLogs:
											data_SaveLogFileName = json.load(fileObjectConfigSaveDetailedLogs)

											# Iterating through the json dict of detailed save again
											for commandString in data_SaveLogFileName['collect_ADL_specific_logs']:

												# Dump only if file name matches this file name
												if (data_SaveLogFileName['collect_ADL_specific_logs'][commandString] == comparisonFileName):
													logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file re-captured due to diff: " + comparisonFileName)
													logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": commandString: " + str(commandString))
													outputString = execute_Command(commandString)

													logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): file re-captured due to diff")
													append_String_To_File(outputString, os.path.join(iterationFolderCompletePath, comparisonFileName + "_recaptured"))
													retain_log_files(iterationFolderCompletePath)

													if (stop_on_error_String != "STOP_ON_ERROR_NO"):
														logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": before writing file for stop_on_error for: " + commandString)

														try:
															with open(constants.STOP_ON_ERROR_FILE,"w") as fileObjectStopOnError:
																fileObjectStopOnError.write (str("STOP_ON_ERROR"))

														except (OSError, IOError) as exception:
															logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

														logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": after writing files for stop_on_error")

											for commandString in data_SaveLogFileName['save_detailed_logs_only_On_FF']:

												# Dump only if file name matches this file name
												if (data_SaveLogFileName['save_detailed_logs_only_On_FF'][commandString] == comparisonFileName):
													logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file re-captured due to diff: " + comparisonFileName)
													logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": commandString: " + str(commandString))
													outputString = execute_Command(commandString)

													logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): file re-captured due to diff")
													append_String_To_File(outputString, os.path.join(iterationFolderCompletePath, comparisonFileName + "_recaptured"))
													retain_log_files(iterationFolderCompletePath)

													if (stop_on_error_String != "STOP_ON_ERROR_NO"):
														logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": before writing file for stop_on_error for: " + commandString)

														try:
															with open(constants.STOP_ON_ERROR_FILE,"w") as fileObjectStopOnError:
																fileObjectStopOnError.write (str("STOP_ON_ERROR"))

														except (OSError, IOError) as exception:
															logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

														logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": after writing files for stop_on_error")

											for commandString in data_SaveLogFileName['save_detailed_logs_for_WWAN']:

												# Dump only if file name matches this file name
												if (data_SaveLogFileName['save_detailed_logs_for_WWAN'][commandString] == comparisonFileName):
													logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file re-captured due to diff: " + comparisonFileName)
													logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": commandString: " + str(commandString))
													outputString = execute_Command(commandString)

													logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): file re-captured due to diff")
													append_String_To_File(outputString, os.path.join(iterationFolderCompletePath, comparisonFileName + "_recaptured"))
													retain_log_files(iterationFolderCompletePath)

													if (stop_on_error_String != "STOP_ON_ERROR_NO"):
														logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": before writing file for stop_on_error for: " + commandString)

														try:
															with open(constants.STOP_ON_ERROR_FILE,"w") as fileObjectStopOnError:
																fileObjectStopOnError.write (str("STOP_ON_ERROR"))

														except (OSError, IOError) as exception:
															logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

														logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": after writing files for stop_on_error")

											for commandString in data_SaveLogFileName['save_detailed_logs_RVP_and_FF']:

												# Dump only if file name matches this file name
												if (data_SaveLogFileName['save_detailed_logs_RVP_and_FF'][commandString] == comparisonFileName):
													logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): file re-captured due to diff: " + comparisonFileName)
													logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": commandString: " + str(commandString))
													outputString = execute_Command(commandString)

													append_String_To_File(outputString, os.path.join(iterationFolderCompletePath, comparisonFileName + "_recaptured"))
													retain_log_files(iterationFolderCompletePath)

													if (stop_on_error_String != "STOP_ON_ERROR_NO"):
														logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": before writing file for stop_on_error for: " + commandString)

														try:
															with open(constants.STOP_ON_ERROR_FILE,"w") as fileObjectStopOnError:
																fileObjectStopOnError.write (str("STOP_ON_ERROR"))

														except (OSError, IOError) as exception:
															logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

														logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": after writing files for stop_on_error")

									except (OSError, IOError, KeyError, json.decoder.JSONDecodeError) as exception:
										logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

										logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": exiting script")
										exit()

									# Reset the file pointer to start for original file
									hosts0.seek(0)

									# Open recaptured file
									with open(os.path.join(iterationFolderCompletePath, comparisonFileName + "_recaptured"), 'r') as hosts1_recapture:
										# Compare with recaptured file
										logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Before recapture: " + comparisonFileName)

										diff_recapture = difflib.unified_diff(
											hosts0.readlines(),
											hosts1_recapture.readlines(),
											fromfile=(constants.ORIGINAL_FOLDER_NAME),
											tofile=(iterationFolderCompletePath + "/" + comparisonFileName + "_recaptured"),
										)

										# TO DO: optimize this logic, what if delta is too much
										list_diff_files_recapture = list(diff_recapture)

										if len(list_diff_files_recapture) > 0:
											logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": len(list_diff_files_recapture) is non-zero: " + str(len(list_diff_files_recapture)))

											# Dumping the iteration information after comparing re-captured file
											# Syntax: ERROR: filename is changed: iterationfoldername
											append_String_To_File("ERROR: " + comparisonFileName + " is changed: " + iterationFolderCompletePath + "\n", os.path.join(constants.LOG_DIRECTORY_FULL_PATH, constants.ERROR_ITERATIONS_FILE))

											with open(constants.ERROR_DETAILS_FILE, "a") as fileObjectErrorDetails:
												for diff_line_recapture in list_diff_files_recapture:
													fileObjectErrorDetails.write(diff_line_recapture)

									hosts1_recapture.close()

								else:
									pass

							hosts1.close()
						hosts0.close()
					else:
						logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file does not exist for comparison in iteration: " + str(os.path.join(iterationFolderCompletePath, comparisonFileName)))
						# Ideally, we should catch this error. Needs test parameters flags to be tracked
						# Commenting out for now
						# append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: ERROR: File does not exist for comparison in iteration: " + comparisonFileName + "\n", os.path.join(constants.LOG_DIRECTORY_FULL_PATH, constants.ERROR_DETAILS_FILE))

				else:
					logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file does not exist for comparison in original: " + str(os.path.join(constants.LOG_DIRECTORY_FULL_PATH, constants.ORIGINAL_FOLDER_NAME, comparisonFileName)))
					# Ideally, we should catch this error. Needs test parameters flags to be tracked
					# Commenting out for now
					# append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: ERROR: File does not exist for comparison in original: " + comparisonFileName + "\n", os.path.join(constants.LOG_DIRECTORY_FULL_PATH, constants.ERROR_DETAILS_FILE))

	except (OSError, IOError, KeyError, json.decoder.JSONDecodeError) as exception:
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": exiting script")
		exit()

	# store end time
	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Calling sync")
	execute_Command("sync")
	endTime = time.time()

	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Time taken for function execution: " + str(int(endTime-startTime)))

	if int(endTime-startTime) > constants.TIME_FIFTEEN_SECONDS:
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): execution time for " + functionName + " is more than " + str(constants.TIME_FIFTEEN_SECONDS))
		append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno)  + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: ERROR: execution time for " + functionName + " is more than " + str(constants.TIME_FIFTEEN_SECONDS) + "\n", os.path.join(constants.LOG_DIRECTORY_FULL_PATH, constants.ERROR_DETAILS_FILE))
		retain_log_files(iterationFolderCompletePath)

def save_quick_logs(iterationFolderCompletePath):
	"""
	Purpose: Save brief information from DUT

	Parameters: iterationFolderCompletePath: String: indicates iteration's folder which contains log files. This includes complete path

	Returns: None
    """

	""" Create frame object """
	frameObj = currentframe()

	""" String to track current function name """
	functionName = str(frameObj.f_code.co_name) + "()" # Function name

	# store starting time
	startTime = time.time()

	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Entered")

	if os.path.isdir(iterationFolderCompletePath):
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": directory exists: " + iterationFolderCompletePath)
	else:
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": directory does not exist: " + iterationFolderCompletePath)

		try:
			os.mkdir(iterationFolderCompletePath)
		except (FileNotFoundError,OSError, IOError) as exception:
			logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

			logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": exiting script")
			exit()

	if os.path.isfile(constants.JSON_CONFIG_FILE_SAVE_QUICK_LOGS):
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file exists: " + constants.JSON_CONFIG_FILE_SAVE_QUICK_LOGS)
	else:
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file does not exist: " + constants.JSON_CONFIG_FILE_SAVE_QUICK_LOGS)
		return

	save_dmesg_logs(iterationFolderCompletePath)
	login_to_DUT(iterationFolderCompletePath)
	parse_JSON_save_quick_log_files (iterationFolderCompletePath)
	parse_JSON_save_count_values (iterationFolderCompletePath)

def parse_JSON_save_quick_log_files(iterationFolderCompletePath):
	"""
	Purpose: Save log files from DUT

	Parameters: iterationFolderCompletePath: String: indicates iteration's folder which contains log files. This includes complete path

	Returns: None
    """

	""" Create frame object """
	frameObj = currentframe()

	""" String to track current function name """
	functionName = str(frameObj.f_code.co_name) + "()" # Function name

	# store starting time
	startTime = time.time()

	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Entered")

	if os.path.isdir(iterationFolderCompletePath):
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": directory exists: " + iterationFolderCompletePath)
	else:
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": directory does not exist: " + iterationFolderCompletePath)

		try:
			os.mkdir(iterationFolderCompletePath)
		except (FileNotFoundError,OSError, IOError) as exception:
			logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

			logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": exiting script")
			exit()

	if os.path.isfile(constants.JSON_CONFIG_FILE_SAVE_QUICK_LOGS):
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file exists: " + constants.JSON_CONFIG_FILE_SAVE_QUICK_LOGS)
	else:
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file does not exist: " + constants.JSON_CONFIG_FILE_SAVE_QUICK_LOGS)
		return

	# Also store quick logs for summary
	try:
		with open(constants.JSON_CONFIG_FILE_SAVE_QUICK_LOGS) as fileObjectQuickCommands:
			dataQuickLogFiles = json.load(fileObjectQuickCommands)

			for commandString in dataQuickLogFiles['save_quick_logs_for_tracking']:
				outputString = execute_Command(commandString)
				append_String_To_File(outputString, os.path.join(iterationFolderCompletePath, dataQuickLogFiles['save_quick_logs_for_tracking'][commandString]))

	except (OSError, IOError, KeyError, json.decoder.JSONDecodeError) as exception:
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": exiting script")
		exit()

def parse_JSON_save_count_values(iterationFolderCompletePath):
	"""
	Purpose: Save brief information from DUT

	Parameters: iterationFolderCompletePath: String: indicates iteration's folder which contains log files. This includes complete path

	Returns: None
    """

	""" Create frame object """
	frameObj = currentframe()

	""" String to track current function name """
	functionName = str(frameObj.f_code.co_name) + "()" # Function name

	# store starting time
	startTime = time.time()

	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Entered")

	if os.path.isdir(iterationFolderCompletePath):
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": directory exists: " + iterationFolderCompletePath)
	else:
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": directory does not exist: " + iterationFolderCompletePath)

		try:
			os.mkdir(iterationFolderCompletePath)
		except (FileNotFoundError,OSError, IOError) as exception:
			logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

			logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": exiting script")
			exit()

	if os.path.isfile(constants.JSON_CONFIG_FILE_SAVE_QUICK_LOGS):
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file exists: " + constants.JSON_CONFIG_FILE_SAVE_QUICK_LOGS)
	else:
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file does not exist: " + constants.JSON_CONFIG_FILE_SAVE_QUICK_LOGS)
		return

	# Also store quick logs for summary
	try:
		with open(constants.JSON_CONFIG_FILE_SAVE_QUICK_LOGS) as fileObjectQuickCommands:
			data = json.load(fileObjectQuickCommands)

			# Iterating through the json file. This is dict of dict
			for commandString, list_StopOnError_ExpectedResult_stringMessage in data['save_quick_count_for_tracking_for_nonzero'].items():
				outputString = execute_Command(commandString)

				stop_on_error_String = list_StopOnError_ExpectedResult_stringMessage[0]
				expectedResult_String = list_StopOnError_ExpectedResult_stringMessage[1]
				stringMessage = list_StopOnError_ExpectedResult_stringMessage[2]

				# strip() removes leading/trailing white spaces
				if (outputString.strip().isnumeric()):

					# Ensure these error strings are non-zero
					if int(outputString.strip()) == 0:
						logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): stringMessage: " + stringMessage + " is zero")
						append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno)  + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: ERROR: " + stringMessage + " is zero\n", os.path.join(constants.LOG_DIRECTORY_FULL_PATH, constants.ERROR_DETAILS_FILE))
						retain_log_files(iterationFolderCompletePath)
					else:
						# strip() removes leading/trailing white spaces
						logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": stringMessage: " + stringMessage + " : " + outputString.strip())
						append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno)  + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: " + stringMessage + " : " + outputString.strip() + "\n", os.path.join(constants.LOG_DIRECTORY_FULL_PATH, constants.ERROR_DETAILS_FILE))

				if (str(expectedResult_String) != str(outputString.strip())):
					if (stop_on_error_String != "STOP_ON_ERROR_NO"):
						logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": before writing file for stop_on_error for: " + commandString)

						try:
							with open(constants.STOP_ON_ERROR_FILE,"w") as fileObjectStopOnError:
								fileObjectStopOnError.write (str("STOP_ON_ERROR"))

						except (OSError, IOError) as exception:
							logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

						logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": after writing files for stop_on_error")

			# Iterating through the json file. This is dict of dict
			for commandString, list_StopOnError_ExpectedResult_stringMessage in data['save_quick_string_for_deviation_from_desired'].items():
				outputString = execute_Command(commandString)

				stop_on_error_String = list_StopOnError_ExpectedResult_stringMessage[0]
				expectedResult_String = list_StopOnError_ExpectedResult_stringMessage[1]
				stringMessage = list_StopOnError_ExpectedResult_stringMessage[2]

				if (outputString != None and len (outputString) != 0):
					logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": stringMessage: " + stringMessage + " : " + outputString.strip())
					append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: " + stringMessage + " : " + outputString.strip() + "\n", os.path.join(constants.LOG_DIRECTORY_FULL_PATH, constants.ERROR_DETAILS_FILE))

					if (str(expectedResult_String) != str(outputString.strip())):
						logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": stringMessage: " + stringMessage + ": stop_on_error_String is: " + stop_on_error_String + ": expectedResult_String != outputString")

						if (stop_on_error_String != "STOP_ON_ERROR_NO"):
							logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": stop_on_error_String is not STOP_ON_ERROR_NO")

							logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": before writing file for stop_on_error for: " + commandString)

							try:
								with open(constants.STOP_ON_ERROR_FILE,"w") as fileObjectStopOnError:
									fileObjectStopOnError.write (str("STOP_ON_ERROR"))

							except (OSError, IOError) as exception:
								logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

							logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": after writing files for stop_on_error")

			# Iterating through the json file. This is dict of dict
			for commandString, list_StopOnError_ExpectedResult_stringMessage in data['save_quick_count_for_deviation_from_desired'].items():
				outputString = execute_Command(commandString)

				stop_on_error_String = list_StopOnError_ExpectedResult_stringMessage[0]
				expectedResult_String = list_StopOnError_ExpectedResult_stringMessage[1]
				stringMessage = list_StopOnError_ExpectedResult_stringMessage[2]

				if (str(expectedResult_String) != str(outputString.strip())):
					logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): expectedResult_String != outputString")
					append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: ERROR: " + stringMessage + " does not meet desired count criteria\n", os.path.join(constants.LOG_DIRECTORY_FULL_PATH, constants.ERROR_DETAILS_FILE))
					retain_log_files(iterationFolderCompletePath)

					if (stop_on_error_String != "STOP_ON_ERROR_NO"):
						logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": before writing file for stop_on_error for: " + commandString)

						try:
							with open(constants.STOP_ON_ERROR_FILE,"w") as fileObjectStopOnError:
								fileObjectStopOnError.write (str("STOP_ON_ERROR"))

						except (OSError, IOError) as exception:
							logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

						logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": after writing files for stop_on_error")

	except (OSError, IOError, KeyError, json.decoder.JSONDecodeError) as exception:
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": exiting script")
		exit()

	# store end time
	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Calling sync")
	execute_Command("sync")
	endTime = time.time()

	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Time taken for function execution: " + str(int(endTime-startTime)))

	if int(endTime-startTime) > constants.TIME_FIFTEEN_SECONDS:
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): execution time for " + functionName + " is more than " + str(constants.TIME_FIFTEEN_SECONDS))
		append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno)  + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: ERROR: execution time for " + functionName + " is more than " + str(constants.TIME_FIFTEEN_SECONDS) + "\n", os.path.join(constants.LOG_DIRECTORY_FULL_PATH, constants.ERROR_DETAILS_FILE))
		retain_log_files(iterationFolderCompletePath)

def perform_checks_for_suspend_resume(iterationFolderCompletePath):
	"""
	Purpose: Save brief summary of detailed errors from DUT

	Parameters: None

	Returns: None
    """

	""" Create frame object """
	frameObj = currentframe()

	""" String to track current function name """
	functionName = str(frameObj.f_code.co_name) + "()" # Function name

	# store starting time
	startTime = time.time()

	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Entered")
	try:
		if os.path.isfile(os.path.join(iterationFolderCompletePath, "package_cstate_show.txt")):
			with open(os.path.join(iterationFolderCompletePath, "package_cstate_show.txt"), "r") as fileObject_package_cstate_show:

				string_package_cstate_show_File = fileObject_package_cstate_show.read()

				TOTAL_PC2_ENTRY_COUNT=string_package_cstate_show_File.count('Package C2 ')
				if TOTAL_PC2_ENTRY_COUNT != 0:
					pass
				else:
					logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): package_cstate_show.txt: TOTAL_PC2_ENTRY_COUNT is zero")
					append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno)  + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: ERROR: package_cstate_show.txt: Package C2 entry is not present\n", constants.ERROR_DETAILS_FILE)
					retain_log_files(iterationFolderCompletePath)

				TOTAL_PC3_ENTRY_COUNT=string_package_cstate_show_File.count('Package C3 ')
				if TOTAL_PC3_ENTRY_COUNT != 0:
					pass
				else:
					logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): package_cstate_show.txt: TOTAL_PC3_ENTRY_COUNT is zero")
					append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: ERROR: package_cstate_show.txt: Package C3 entry is not present\n", constants.ERROR_DETAILS_FILE)
					retain_log_files(iterationFolderCompletePath)

				TOTAL_PC6_ENTRY_COUNT=string_package_cstate_show_File.count('Package C6 ')
				if TOTAL_PC6_ENTRY_COUNT != 0:
					pass
				else:
					logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): package_cstate_show.txt: TOTAL_PC6_ENTRY_COUNT is zero")
					append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: ERROR: package_cstate_show.txt: Package C6 entry is not present\n", constants.ERROR_DETAILS_FILE)
					retain_log_files(iterationFolderCompletePath)

				TOTAL_PC7_ENTRY_COUNT=string_package_cstate_show_File.count('Package C7 ')
				if TOTAL_PC7_ENTRY_COUNT != 0:
					pass
				else:
					logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): package_cstate_show.txt: TOTAL_PC7_ENTRY_COUNT is zero")
					append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: ERROR: package_cstate_show.txt: Package C7 entry is not present\n", constants.ERROR_DETAILS_FILE)
					retain_log_files(iterationFolderCompletePath)

				TOTAL_PC8_ENTRY_COUNT=string_package_cstate_show_File.count('Package C8 ')
				if TOTAL_PC8_ENTRY_COUNT != 0:
					pass
				else:
					logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): package_cstate_show.txt: TOTAL_PC8_ENTRY_COUNT is zero")
					append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: ERROR: package_cstate_show.txt: Package C8 entry is not present\n", constants.ERROR_DETAILS_FILE)
					retain_log_files(iterationFolderCompletePath)

				TOTAL_PC9_ENTRY_COUNT=string_package_cstate_show_File.count('Package C9 ')
				if TOTAL_PC9_ENTRY_COUNT != 0:
					pass
				else:
					logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): package_cstate_show.txt: TOTAL_PC9_ENTRY_COUNT is zero")
					append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: ERROR: package_cstate_show.txt: Package C9 entry is not present\n", constants.ERROR_DETAILS_FILE)
					retain_log_files(iterationFolderCompletePath)

				TOTAL_PC10_ENTRY_COUNT=string_package_cstate_show_File.count('Package C10 ')
				if TOTAL_PC10_ENTRY_COUNT != 0:
					pass
				else:
					logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): package_cstate_show.txt: TOTAL_PC10_ENTRY_COUNT is zero")
					append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: ERROR: package_cstate_show.txt: Package C10 entry is not present\n", constants.ERROR_DETAILS_FILE)
					retain_log_files(iterationFolderCompletePath)

				# Check if PC10 entry is non-zero: Package C10 : 0x0
				# For suspend-resume operations, Package C10 entry must be non-zero
				# TGL/JSL+: Package C10 : 0; Package C10 : 3379142150
				# CML Helios/Drallion: Package C10 : 0x0; Package C10 : 0x41fc9fee0
				# "grep -w" matches the whole string
				TOTAL_PC10_ZERO_ENTRY_COUNT_0X0=string_package_cstate_show_File.count('Package C10 : 0x0')
				TOTAL_PC10_ZERO_ENTRY_COUNT_0=string_package_cstate_show_File.count('Package C10 : 0')

				TOTAL_PC10_ZERO_ENTRY_COUNT = TOTAL_PC10_ZERO_ENTRY_COUNT_0X0 + TOTAL_PC10_ZERO_ENTRY_COUNT_0
				if TOTAL_PC10_ZERO_ENTRY_COUNT == 0:
					# logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": package_cstate_show.txt: TOTAL_PC10_ZERO_ENTRY_COUNT: " + str(TOTAL_PC10_ZERO_ENTRY_COUNT))
					pass
				else:
					logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): package_cstate_show.txt: Package C10 non-zero entry is not present")
					append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: ERROR: package_cstate_show.txt: Package C10 non-zero entry is not present\n", constants.ERROR_DETAILS_FILE)

					retain_log_files(iterationFolderCompletePath)

		else:
			logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): package_cstate_show.txt file is NOT present")
			append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: ERROR: package_cstate_show.txt is NOT present\n", constants.ERROR_DETAILS_FILE)
			retain_log_files(iterationFolderCompletePath)

	except (OSError, IOError, KeyError, json.decoder.JSONDecodeError) as exception:
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

	try:
		if os.path.isfile(os.path.join(iterationFolderCompletePath, "package_cstate_show_C10.txt")):
			if os.path.isfile(os.path.join(constants.LOG_DIRECTORY_FULL_PATH, constants.ORIGINAL_FOLDER_NAME, "package_cstate_show_C10.txt")):

				with open(os.path.join(iterationFolderCompletePath, "package_cstate_show_C10.txt"), "r") as fileObject_iteration_package_cstate_show_C10:
					now_package_cstate_show_C10 = fileObject_iteration_package_cstate_show_C10.read()

					with open(os.path.join(constants.LOG_DIRECTORY_FULL_PATH, constants.ORIGINAL_FOLDER_NAME, "package_cstate_show_C10.txt"), "r") as fileObject_original_package_cstate_show_C10:
						original_package_cstate_show_C10 = fileObject_original_package_cstate_show_C10.read()

						if now_package_cstate_show_C10 == original_package_cstate_show_C10:
							logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": " +  iterationFolderCompletePath + ": calling retain_log_files(): package_cstate_show_C10.txt: Package C10 entry is NOT changed from previous iteration")
							append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: ERROR: package_cstate_show_C10.txt: Package C10 entry is NOT changed from previous iteration\n", constants.ERROR_DETAILS_FILE)
							retain_log_files(iterationFolderCompletePath)
						else:
							logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": package_cstate_show_C10.txt: Package C10 entry is changed from previous iteration")

				# Copy this iteration's PC10 file as original PC10
				shutil.copy(os.path.join(iterationFolderCompletePath, "package_cstate_show_C10.txt"), os.path.join(constants.LOG_DIRECTORY_FULL_PATH, constants.ORIGINAL_FOLDER_NAME, "package_cstate_show_C10.txt"))

			else:
				logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): package_cstate_show_C10.txt file is NOT present in original")
				append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: ERROR: package_cstate_show_C10.txt is NOT present in original\n", constants.ERROR_DETAILS_FILE)
				retain_log_files(iterationFolderCompletePath)

		else:
			logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): package_cstate_show_C10.txt file is NOT present in iteration")
			append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: ERROR: package_cstate_show_C10.txt is NOT present in iteration\n", constants.ERROR_DETAILS_FILE)
			retain_log_files(iterationFolderCompletePath)

	except (OSError, IOError, KeyError, json.decoder.JSONDecodeError) as exception:
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

	try:
		if os.path.isfile(os.path.join(iterationFolderCompletePath, "suspend_stress_test_log.txt")):

			with open(os.path.join(iterationFolderCompletePath, "suspend_stress_test_log.txt"), "r") as fileObject_suspend_stress_test_log:

				string_suspend_stress_test_log = fileObject_suspend_stress_test_log.read()

				TOTAL_SUSPEND_FAILED=string_suspend_stress_test_log.count('Suspend failed')
				if TOTAL_SUSPEND_FAILED == 0:
					logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": TOTAL_SUSPEND_FAILED: " + str(TOTAL_SUSPEND_FAILED))
				else:
					logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): Suspend failed is present")
					append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: ERROR: suspend_stress_test_log.txt: Suspend failed present\n", constants.ERROR_DETAILS_FILE)
					retain_log_files(iterationFolderCompletePath)

				# Premature wakes: 0
				# Late wakes: 0
				# Suspend failures: 0
				# Wakealarm errors: 0
				# Firmware log errors: 0
				# s0ix errors: 1
				TOTAL_PREMATURE_WAKES_ZERO=string_suspend_stress_test_log.count('Premature wakes: 0')
				if TOTAL_PREMATURE_WAKES_ZERO != 0:
					pass
				else:
					logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): suspend_stress_test_log.txt: premature wakes is non-zero")
					append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: ERROR: suspend_stress_test_log.txt: premature wakes is non-zero\n", constants.ERROR_DETAILS_FILE)
					retain_log_files(iterationFolderCompletePath)

				TOTAL_LATE_WAKES_ZERO=string_suspend_stress_test_log.count('Late wakes: 0')
				if TOTAL_LATE_WAKES_ZERO != 0:
					pass
				else:
					logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): suspend_stress_test_log.txt: late wakes is non-zero")
					append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: ERROR: suspend_stress_test_log.txt: late wakes is non-zero\n", constants.ERROR_DETAILS_FILE)
					retain_log_files(iterationFolderCompletePath)

				TOTAL_SUSPEND_FAILURE_ZERO=string_suspend_stress_test_log.count('Suspend failures: 0')
				if TOTAL_SUSPEND_FAILURE_ZERO != 0:
					pass
				else:
					logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): suspend_stress_test_log.txt: suspend failures is non-zero")
					append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: ERROR: suspend_stress_test_log.txt: suspend failures is non-zero\n", constants.ERROR_DETAILS_FILE)
					retain_log_files(iterationFolderCompletePath)

				TOTAL_WAKEALARM_ERRORS_ZERO=string_suspend_stress_test_log.count('Wakealarm errors: 0')
				if TOTAL_WAKEALARM_ERRORS_ZERO != 0:
					pass
				else:
					logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): suspend_stress_test_log.txt: wakealarm errors is non-zero")
					append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: ERROR: suspend_stress_test_log.txt: wakealarm errors is non-zero\n", constants.ERROR_DETAILS_FILE)
					retain_log_files(iterationFolderCompletePath)

				TOTAL_FIRMWARE_LOG_ERRORS_ZERO=string_suspend_stress_test_log.count('Firmware log errors: 0')
				if TOTAL_FIRMWARE_LOG_ERRORS_ZERO != 0:
					pass
				else:
					logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): suspend_stress_test_log.txt: Firmware log errors is non-zero")
					append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: ERROR: suspend_stress_test_log.txt: firmware log errors is non-zero\n", constants.ERROR_DETAILS_FILE)
					retain_log_files(iterationFolderCompletePath)

				TOTAL_S0ix_ERRORS_ZERO=string_suspend_stress_test_log.count('s0ix errors: 0')
				if TOTAL_S0ix_ERRORS_ZERO != 0:
					pass
				else:
					logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): suspend_stress_test_log.txt: s0ix errors is non-zero")
					append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: ERROR: suspend_stress_test_log.txt: s0ix errors is non-zero\n", constants.ERROR_DETAILS_FILE)
					retain_log_files(iterationFolderCompletePath)

				TOTAL_EC_REPORTED_S0ix_ERROR=string_suspend_stress_test_log.count('EC reported S0ix failure')
				if TOTAL_EC_REPORTED_S0ix_ERROR == 0:
					pass
				else:
					logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): suspend_stress_test_log.txt: EC reported S0ix failure is non-zero")
					append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: ERROR: suspend_stress_test_log.txt: EC reported S0ix failure is non-zero\n", constants.ERROR_DETAILS_FILE)
					retain_log_files(iterationFolderCompletePath)

		else:
			logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): suspend_stress_test_log.txt file is NOT present")
			append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: ERROR: suspend_stress_test_log.txt is NOT present\n", constants.ERROR_DETAILS_FILE)
			retain_log_files(iterationFolderCompletePath)

	except (OSError, IOError, KeyError, json.decoder.JSONDecodeError) as exception:
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

	# https://chromium.googlesource.com/chromiumos/third_party/autotest/+/master/client/cros/power/power_suspend.py

	# [   47.592003] PM: suspend of devices complete after 297.411 msecs
	# [   47.612971] PM: late suspend of devices complete after 20.962 msecs
	# [   47.657905] PM: noirq suspend of devices complete after 16.870 msecs

	# [   51.428696] PM: noirq resume of devices complete after 28.586 msecs
	# [   51.439824] PM: early resume of devices complete after 5.966 msecs
	# [   51.728511] PM: resume of devices complete after 288.682 msecs
	try:
		if os.path.isfile(os.path.join(iterationFolderCompletePath, "dmesg.txt")):

			with open(os.path.join(iterationFolderCompletePath, "dmesg.txt"), "r") as fileObjectdmesg:
				list_dmesgFile = fileObjectdmesg.readlines()

			time_taken_SUSPEND_DEVICES_COMPLETE=0
			time_taken_LATE_SUSPEND_DEVICES_COMPLETE=0
			time_taken_NOIRQ_SUSPEND_DEVICES_COMPLETE=0
			time_taken_total_suspend_time=0

			time_taken_NOIRQ_RESUME_DEVICES_COMPLETE=0
			time_taken_EARLY_RESUME_DEVICES_COMPLETE=0
			time_taken_RESUME_DEVICES_COMPLETE=0
			time_taken_total_resume_time=0

			for dmesg_line in list_dmesgFile:

				if "PM: suspend of devices complete after" in dmesg_line:
					try:
						time_taken_SUSPEND_DEVICES_COMPLETE=float((dmesg_line.split("PM: suspend of devices complete after")[1]).replace(" msecs", ""))
						#logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": dmesg.txt: time_taken_SUSPEND_DEVICES_COMPLETE: " + str(time_taken_SUSPEND_DEVICES_COMPLETE))
					except (IndexError) as exception:
						logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))
					continue

				if "PM: late suspend of devices complete after" in dmesg_line:
					try:
						time_taken_LATE_SUSPEND_DEVICES_COMPLETE=float((dmesg_line.split("PM: late suspend of devices complete after")[1]).replace(" msecs", ""))
						#logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": dmesg.txt: time_taken_LATE_SUSPEND_DEVICES_COMPLETE: " + str(time_taken_LATE_SUSPEND_DEVICES_COMPLETE))
					except (IndexError) as exception:
						logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))
					continue

				if "PM: noirq suspend of devices complete after" in dmesg_line:
					try:
						time_taken_NOIRQ_SUSPEND_DEVICES_COMPLETE=float((dmesg_line.split("PM: noirq suspend of devices complete after")[1]).replace(" msecs", ""))
						#logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": dmesg.txt: time_taken_NOIRQ_SUSPEND_DEVICES_COMPLETE: " + str(time_taken_NOIRQ_SUSPEND_DEVICES_COMPLETE))
					except (IndexError) as exception:
						logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))
					continue

				if "PM: noirq resume of devices complete after" in dmesg_line:
					try:
						time_taken_NOIRQ_RESUME_DEVICES_COMPLETE=float((dmesg_line.split("PM: noirq resume of devices complete after")[1]).replace(" msecs", ""))
						#logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": dmesg.txt: time_taken_NOIRQ_RESUME_DEVICES_COMPLETE: " + str(time_taken_NOIRQ_RESUME_DEVICES_COMPLETE))
					except (IndexError) as exception:
						logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))
					continue

				if "PM: early resume of devices complete after" in dmesg_line:
					try:
						time_taken_EARLY_RESUME_DEVICES_COMPLETE=float((dmesg_line.split("PM: early resume of devices complete after")[1]).replace(" msecs", ""))
						#logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": dmesg.txt: time_taken_EARLY_RESUME_DEVICES_COMPLETE: " + str(time_taken_EARLY_RESUME_DEVICES_COMPLETE))
					except (IndexError) as exception:
						logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))
					continue

				if "PM: resume of devices complete after" in dmesg_line:
					try:
						time_taken_RESUME_DEVICES_COMPLETE=float((dmesg_line.split("PM: resume of devices complete after")[1]).replace(" msecs", ""))
						#logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": dmesg.txt: time_taken_RESUME_DEVICES_COMPLETE: " + str(time_taken_RESUME_DEVICES_COMPLETE))
					except (IndexError) as exception:
						logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))
					continue

			time_taken_total_suspend_time = time_taken_SUSPEND_DEVICES_COMPLETE + time_taken_LATE_SUSPEND_DEVICES_COMPLETE + time_taken_NOIRQ_SUSPEND_DEVICES_COMPLETE
			# logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": dmesg.txt: time_taken_total_suspend_time: " + str(time_taken_total_suspend_time))

			if int(time_taken_total_suspend_time) <= 0 and int(time_taken_total_suspend_time) >= constants.SUSPEND_TIME_TARGET_MSECS:
				logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): dmesg.txt: suspend takes more than " + str(constants.SUSPEND_TIME_TARGET_MSECS) + " msecs")
				append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: ERROR: dmesg.txt: suspend takes more than " + str(constants.SUSPEND_TIME_TARGET_MSECS) + " msecs\n", constants.ERROR_DETAILS_FILE)
				retain_log_files(iterationFolderCompletePath)
			else:
				logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": dmesg.txt: suspend takes less than " + str(constants.SUSPEND_TIME_TARGET_MSECS) + " msecs")

			time_taken_total_resume_time = time_taken_NOIRQ_RESUME_DEVICES_COMPLETE + time_taken_NOIRQ_RESUME_DEVICES_COMPLETE + time_taken_RESUME_DEVICES_COMPLETE
			# logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": dmesg.txt: time_taken_total_resume_time: " + str(time_taken_total_resume_time))

			if int(time_taken_total_resume_time) <= 0 and int(time_taken_total_resume_time) >= constants.RESUME_TIME_TARGET_MSECS:
				logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): dmesg.txt: resume takes more than " + str(constants.RESUME_TIME_TARGET_MSECS) + " msecs")
				append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: ERROR: dmesg.txt: resume takes more than " + str(constants.RESUME_TIME_TARGET_MSECS) + " msecs\n", constants.ERROR_DETAILS_FILE)
				retain_log_files(iterationFolderCompletePath)
			else:
				logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": dmesg.txt: resume takes less than " + str(constants.RESUME_TIME_TARGET_MSECS) + " msecs")

		else:
			logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): dmesg.txt file is NOT present in iteration")
			append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: ERROR: dmesg.txt is NOT present in iteration\n", constants.ERROR_DETAILS_FILE)
			retain_log_files(iterationFolderCompletePath)

	except (OSError, IOError, KeyError, json.decoder.JSONDecodeError) as exception:
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

	# https://chromium.googlesource.com/chromiumos/third_party/autotest/+/master/client/cros/power/power_suspend.py
	# start_suspend_time=47.290617
	# end_suspend_time=47.657907
	# start_resume_time=51.400107
	# end_resume_time=51.730261
	try:
		if os.path.isfile(os.path.join(iterationFolderCompletePath, "last_resume_timings.txt")):

			with open(os.path.join(iterationFolderCompletePath, "last_resume_timings.txt"), "r") as last_resume_timings_fileObject:
				list_last_resume_timings = last_resume_timings_fileObject.readlines()

			time_taken_start_suspend_time=0
			time_taken_end_suspend_time=0
			time_taken_start_resume_time=0
			time_taken_end_resume_time=0
			time_taken_total_suspend_time=0
			time_taken_total_resume_time=0

			for line_last_resume_timings in list_last_resume_timings:
				if "start_suspend_time=" in line_last_resume_timings:
					try:
						time_taken_start_suspend_time=float(line_last_resume_timings.split("start_suspend_time=")[1])
					except (ValueError, IndexError) as exception:
						logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))
					continue

				if "end_suspend_time=" in line_last_resume_timings:
					try:
						time_taken_end_suspend_time=float(line_last_resume_timings.split("end_suspend_time=")[1])
					except (ValueError, IndexError) as exception:
						logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))
					continue

				if "start_resume_time=" in line_last_resume_timings:
					try:
						time_taken_start_resume_time=float(line_last_resume_timings.split("start_resume_time=")[1])
					except (ValueError, IndexError) as exception:
						logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))
					continue

				if "end_resume_time=" in line_last_resume_timings:
					try:
						time_taken_end_resume_time=float(line_last_resume_timings.split("end_resume_time=")[1])
					except (ValueError, IndexError) as exception:
						logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))
					continue

			time_taken_total_suspend_time = time_taken_end_suspend_time - time_taken_start_suspend_time

			if int(time_taken_total_suspend_time) <= 0 and int(time_taken_total_suspend_time) >= constants.SUSPEND_TIME_TARGET_MSECS:
				logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): last_resume_timings.txt: suspend takes more than " + str(constants.SUSPEND_TIME_TARGET_MSECS) + " msecs")
				append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: ERROR: last_resume_timings.txt: suspend takes more than " + str(constants.SUSPEND_TIME_TARGET_MSECS) + " msecs\n", constants.ERROR_DETAILS_FILE)
				retain_log_files(iterationFolderCompletePath)
			else:
				logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": last_resume_timings.txt: suspend takes less than " + str(constants.SUSPEND_TIME_TARGET_MSECS) + " msecs")

			time_taken_total_resume_time = time_taken_end_resume_time - time_taken_start_resume_time

			if int(time_taken_total_resume_time) <= 0 and int(time_taken_total_resume_time) >= constants.RESUME_TIME_TARGET_MSECS:
				logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): last_resume_timings.txt: resume takes more than " + str(constants.RESUME_TIME_TARGET_MSECS) + " msecs")
				append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: ERROR: last_resume_timings.txt: resume takes more than " + str(constants.RESUME_TIME_TARGET_MSECS) + " msecs\n", constants.ERROR_DETAILS_FILE)
				retain_log_files(iterationFolderCompletePath)
			else:
				logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": last_resume_timings.txt: resume takes less than " + str(constants.RESUME_TIME_TARGET_MSECS) + " msecs")

		else:
			logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): last_resume_timings.txt file is NOT present in iteration")
			append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: ERROR: last_resume_timings.txt is NOT present in iteration\n", constants.ERROR_DETAILS_FILE)
			retain_log_files(iterationFolderCompletePath)

	except (OSError, IOError, KeyError, json.decoder.JSONDecodeError) as exception:
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

	try:
		if os.path.isfile(os.path.join(iterationFolderCompletePath, "slp_s0_residency_usec.txt")):
			if os.path.isfile(os.path.join(constants.LOG_DIRECTORY_FULL_PATH, constants.ORIGINAL_FOLDER_NAME, "slp_s0_residency_usec.txt")):

				with open(os.path.join(iterationFolderCompletePath, "slp_s0_residency_usec.txt"), "r") as fileObject_iteration_slp_s0_residency_usec:
					now_slp_s0_residency_usec = fileObject_iteration_slp_s0_residency_usec.read()

					with open(os.path.join(constants.LOG_DIRECTORY_FULL_PATH, constants.ORIGINAL_FOLDER_NAME, "slp_s0_residency_usec.txt"), "r") as fileObject_original_slp_s0_residency_usec:
						original_slp_s0_residency_usec = fileObject_original_slp_s0_residency_usec.read()

						logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": slp_s0_residency_usec.txt: now_slp_s0_residency_usec: " + str(now_slp_s0_residency_usec))

						if now_slp_s0_residency_usec == 0:
							logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): slp_s0_residency_usec.txt: slp_s0_residency_usec is zero")
							append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: ERROR: slp_s0_residency_usec.txt: slp_s0_residency_usec is zero\n", constants.ERROR_DETAILS_FILE)
							retain_log_files(iterationFolderCompletePath)

						if now_slp_s0_residency_usec == original_slp_s0_residency_usec:
							logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): slp_s0_residency_usec.txt: slp_s0_residency_usec is NOT changed from previous iteration")
							append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: ERROR: slp_s0_residency_usec.txt: slp_s0_residency_usec is NOT changed from previous iteration\n", constants.ERROR_DETAILS_FILE)
							retain_log_files(iterationFolderCompletePath)

			else:
				logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): slp_s0_residency_usec.txt file is NOT present in original")
				append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: ERROR: slp_s0_residency_usec.txt is NOT present in original\n", constants.ERROR_DETAILS_FILE)
				retain_log_files(iterationFolderCompletePath)

			# Copy this iteration's PC10 file as original PC10
			shutil.copy(os.path.join(iterationFolderCompletePath, "slp_s0_residency_usec.txt"), os.path.join(constants.LOG_DIRECTORY_FULL_PATH, constants.ORIGINAL_FOLDER_NAME, "slp_s0_residency_usec.txt"))

		else:
			logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): slp_s0_residency_usec.txt file is NOT present in iteration")
			append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: ERROR: slp_s0_residency_usec.txt is NOT present in iteration\n", constants.ERROR_DETAILS_FILE)
			retain_log_files(iterationFolderCompletePath)

	except (OSError, IOError, KeyError, json.decoder.JSONDecodeError) as exception:
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

	try:
		# Check supported substate_residencies
		with open(constants.JSON_CONFIG_FILE_TEST_PARAMETERS) as fileObjectConfigFileTestParameters:
			dataTestParameters = json.load(fileObjectConfigFileTestParameters)

			# Iterating through the json dict
			for stringParameter in dataTestParameters:
				# Perform case-insensitive comparison
				if (stringParameter.casefold() == "substate_residencies_supported".casefold()):
					list_substate_residencies_supported = dataTestParameters[stringParameter]
					logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": list_substate_residencies_supported: " + str(list_substate_residencies_supported))

	except (OSError, IOError, KeyError, json.decoder.JSONDecodeError) as exception:
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": exiting script")
		exit()

	try:
		# ADL
		# Substate   Residency
		#S0i2.0     0
		#S0i3.0     0

		# TGL
		# status substate residency
		# Enabled  S0i2.0 0
		# Enabled  S0i2.1 0
		#		 S0i2.2 0
		# Enabled  S0i3.0 0
		# Enabled  S0i3.1 0
		# Enabled  S0i3.2 196363
		#		 S0i3.3 0
		#		 S0i3.4 0
		if os.path.isfile(os.path.join(iterationFolderCompletePath, "substate_residencies_original.txt")):

			if os.path.isfile(os.path.join(constants.LOG_DIRECTORY_FULL_PATH, "substate_residencies_original.txt")):

				with open(os.path.join(iterationFolderCompletePath, "substate_residencies_original.txt"), "r") as fileObject_now_substate_residencies:
					now_substate_residencies_list = fileObject_now_substate_residencies.readlines()

					with open(os.path.join(constants.LOG_DIRECTORY_FULL_PATH, "substate_residencies_original.txt"), "r") as fileObject_original_substate_residencies:
						original_substate_residencies_list = fileObject_original_substate_residencies.readlines()

						for substate_residencies_entry in list_substate_residencies_supported:
							logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": substate_residencies_entry: " + substate_residencies_entry)

							# Checks if substate residencies are present
							substate_residencies_entry_Present = 0

							for now_substate_residencies_line in now_substate_residencies_list:
								# logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": substate_residencies_original.txt: now_substate_residencies_line: " + str(now_substate_residencies_line))

								if substate_residencies_entry in now_substate_residencies_line:
									substate_residencies_entry_Present = 1
									logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": substate_residencies_original.txt: contains " + substate_residencies_entry)

								for original_substate_residencies_line in original_substate_residencies_list:
									# logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": substate_residencies_original.txt: original_substate_residencies_line: " + str(original_substate_residencies_line))

									if substate_residencies_entry in now_substate_residencies_line and substate_residencies_entry in original_substate_residencies_line:
										substate_residencies_entry_now_Value = int(now_substate_residencies_line.split(substate_residencies_entry)[1].strip())
										substate_residencies_entry_original_Value = int(original_substate_residencies_line.split(substate_residencies_entry)[1].strip())

										logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": substate_residencies_original.txt: substate_residencies_entry_original_Value: " + str(substate_residencies_entry_original_Value))
										logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": substate_residencies_original.txt: substate_residencies_entry_now_Value: " + str(substate_residencies_entry_now_Value))

										# Both now and previous are zero
										if substate_residencies_entry_now_Value == 0 and substate_residencies_entry_original_Value == 0:
											logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): substate_residencies_original.txt: " + substate_residencies_entry + " is zero like previous iteration")
											append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: ERROR: substate_residencies_original.txt: " + substate_residencies_entry + " is zero like previous iteration\n", constants.ERROR_DETAILS_FILE)
											retain_log_files(iterationFolderCompletePath)

										# now is zero and previous is not zero
										if substate_residencies_entry_now_Value == 0 and substate_residencies_entry_now_Value != substate_residencies_entry_original_Value:
											logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): substate_residencies_original.txt: " + substate_residencies_entry + " has become zero in this iteration")
											append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: ERROR: substate_residencies_original.txt: " + substate_residencies_entry + " has become zero in this iteration\n", constants.ERROR_DETAILS_FILE)
											retain_log_files(iterationFolderCompletePath)

										# now is non-zero and previous is zero
										if substate_residencies_entry_now_Value != 0 and substate_residencies_entry_original_Value == 0:
											logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": substate_residencies_original.txt: " + substate_residencies_entry + " has become non-zero in this iteration")

										# now is non-zero and previous is non-zero, but both are same!
										if substate_residencies_entry_now_Value != 0 and substate_residencies_entry_original_Value != 0 and substate_residencies_entry_now_Value == substate_residencies_entry_original_Value:
											logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): substate_residencies_original.txt: " + substate_residencies_entry + " is non-zero and has NOT changed from previous iteration")
											append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: ERROR: substate_residencies_original.txt: " + substate_residencies_entry + " is non-zero and has NOT changed from previous iteration\n", constants.ERROR_DETAILS_FILE)
											retain_log_files(iterationFolderCompletePath)

										# now is non-zero and previous is non-zero, but both are NOT same
										if substate_residencies_entry_now_Value != 0 and substate_residencies_entry_original_Value != 0 and substate_residencies_entry_now_Value != substate_residencies_entry_original_Value:
											logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ":\t" + iterationFolderCompletePath + "\t: substate_residencies_original.txt: " + substate_residencies_entry + " is non-zero and has changed from non-zero previous iteration")

										if substate_residencies_entry_now_Value < 0:
											logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": substate_residencies_original.txt: " + substate_residencies_entry + " is less than zero\n")

							# Check if substate entry is present
							if substate_residencies_entry_Present == 0:
								logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): substate_residencies_original.txt: " + substate_residencies_entry + " entry is NOT present")
								append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": " + iterationFolderCompletePath + ": FOR PCT TRACKING: ERROR: substate_residencies_original.txt: " + substate_residencies_entry + " entry is NOT present\n", constants.ERROR_DETAILS_FILE)
								retain_log_files(iterationFolderCompletePath)

			else:
				logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): substate_residencies_original.txt file is NOT present in folder")
				append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: ERROR: substate_residencies_original.txt is NOT present in original\n", constants.ERROR_DETAILS_FILE)
				retain_log_files(iterationFolderCompletePath)

			# Copy this iteration's file as previous iteration's file
			shutil.copy(os.path.join(iterationFolderCompletePath, "substate_residencies_original.txt"), os.path.join(constants.LOG_DIRECTORY_FULL_PATH, "substate_residencies_original.txt"))

		else:
			logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): substate_residencies_original.txt file is NOT present in iteration")
			append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: ERROR: substate_residencies_original.txt is NOT present in iteration\n", constants.ERROR_DETAILS_FILE)
			retain_log_files(iterationFolderCompletePath)

	except (OSError, IOError, KeyError, json.decoder.JSONDecodeError) as exception:
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

def perform_suspend_resume_quick_tests(stringFolderName_NowTimeDate_PowerCycling, argumentNumberOfIterations):
	"""
	Purpose: Save brief summary of detailed errors from DUT

-	Parameters: 
	stringFolderName_NowTimeDate_PowerCycling: Folder name of power cycling to append to suspend-resume folder
	argumentNumberOfIterations: number of iterations for performing suspend-resume

	Returns: None
    """

	""" Create frame object """
	frameObj = currentframe()

	""" String to track current function name """
	functionName = str(frameObj.f_code.co_name) + "()" # Function name

	# store starting time
	startTime = time.time()

	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Entered")

	for currentIteration in range (argumentNumberOfIterations):

		kill_specific_process("dmesg")
		kill_specific_process("btmon")
		kill_specific_process("tcpdump")

		# Returns a datetime object containing the local date and time
		nowTimeDate = datetime.datetime.now()
		stringFolderName_NowTimeDate = stringFolderName_NowTimeDate_PowerCycling + "_" + str(currentIteration + 1) + "_" + nowTimeDate.strftime("%d%m%Y_%H%M%S") + "_" + constants.STRING_SUSPEND_RESUME_S0ix
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": power cycling folder timestamp calling " + stringFolderName_NowTimeDate_PowerCycling)
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": folder timestamp calling " + stringFolderName_NowTimeDate)

		iterationFolderCompletePath=os.path.join(constants.LOG_DIRECTORY_FULL_PATH, stringFolderName_NowTimeDate)

		try:
			os.mkdir(iterationFolderCompletePath)
		except (FileNotFoundError,OSError, IOError) as exception:
			logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

			logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": exiting script")
			exit()

		# Clear off dmesg logs before we perform test
		execute_Command("dmesg -c")

		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Before suspending: currentIteration: " + str(currentIteration + 1))
		time.sleep(constants.TIME_ONE_SECOND)
		string_suspend_stress_test_log=execute_Command("suspend_stress_test -c 1")

		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": After suspending: currentIteration: " + str(currentIteration + 1))
		time.sleep(constants.TIME_FIVE_SECONDS)

		save_quick_logs(iterationFolderCompletePath)

		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": After calling save_quick_logs()")

		write_string_to_file(string_suspend_stress_test_log, os.path.join(iterationFolderCompletePath, "suspend_stress_test_log.txt"))

		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": After calling write_string_to_file()")

		# Copy iteration's file in parent folder of log location
		if os.path.isfile(os.path.join(iterationFolderCompletePath, "substate_residencies_original.txt")):
			logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": substate_residencies_original.txt present")
			shutil.copy(os.path.join(iterationFolderCompletePath, "substate_residencies_original.txt"), os.path.join(constants.LOG_DIRECTORY_FULL_PATH, "substate_residencies_original.txt"))
			logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": After copying substate_residencies_original.txt")

		perform_checks_for_suspend_resume(iterationFolderCompletePath)

		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": After calling perform_checks_for_suspend_resume()")

		check_errors_during_iteration(iterationFolderCompletePath, constants.ERROR_STRING_DMESG)

		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": After calling check_errors_during_iteration() with constants.ERROR_STRING_DMESG")

		ensure_network_connection(iterationFolderCompletePath)

		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": After calling ensure_network_connection()")

		check_stop_on_error_status()

		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": After calling check_stop_on_error_status()")

		clear_net_log(iterationFolderCompletePath)

		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": After clearing /var/log/net.log")

def save_error_summary():
	"""
	Purpose: Save brief summary of detailed errors from DUT

-	Parameters: None

	Returns: None
    """

	""" Create frame object """
	frameObj = currentframe()

	""" String to track current function name """
	functionName = str(frameObj.f_code.co_name) + "()" # Function name

	# store starting time
	startTime = time.time()

	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": Entered save_error_summary()")
	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Entered")

	kill_specific_process("dmesg")
	kill_specific_process("btmon")
	kill_specific_process("tcpdump")

	check_errors_at_end_of_testing(constants.ERROR_STRING_CONSOLERAMOOPS)
	check_errors_at_end_of_testing(constants.ERROR_STRING_DMESG)
	check_errors_at_end_of_testing(constants.ERROR_STRING_EC)
	check_errors_at_end_of_testing(constants.ERROR_STRING_MMCLI)
	check_errors_at_end_of_testing(constants.ERROR_STRING_TYPECD)

	check_modem_state_at_end_of_testing()

	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": After check_errors_at_end_of_testing()")

	if os.path.isfile(constants.JSON_CONFIG_FILE_COMPARE_LOGS):
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file exists: " + constants.JSON_CONFIG_FILE_COMPARE_LOGS)
	else:
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file does not exist: " + constants.JSON_CONFIG_FILE_COMPARE_LOGS)
		return

	# Count number of files in each of log sub-directories
	log_directory_contents = os.listdir(constants.LOG_DIRECTORY_FULL_PATH)

	for subdirectories in log_directory_contents:
		# Create full path
		fullDirectoryLogPath = os.path.join(constants.LOG_DIRECTORY_FULL_PATH, subdirectories)

		# If entry is a directory then get the list of files in this directory 
		if os.path.isdir(fullDirectoryLogPath):
			log_subdirectory_contents = os.listdir(fullDirectoryLogPath)

			# logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": folder name: " + str(fullDirectoryLogPath) +  ": number of files: " + str(len(log_subdirectory_contents)))

			if (len(log_subdirectory_contents) < constants.NUMBER_OF_LOG_FILES_PER_ITERATION):
				append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ":\t" + str(fullDirectoryLogPath) + "\t: FOR PCT TRACKING: ERROR: number of files is lesser than expected in iteration\n", os.path.join(constants.LOG_DIRECTORY_FULL_PATH, constants.ERROR_DETAILS_FILE))

	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Checking constants.ERROR_DETAILS_FILE")

	list_For_PCT_Tracking = []
	list_Error_Iterations_File = []

	try:
		if os.path.isfile(constants.ERROR_ITERATIONS_FILE):
			logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file exists: " + constants.ERROR_ITERATIONS_FILE)

			# Open this file in read mode
			with open (constants.ERROR_ITERATIONS_FILE, "r") as fileObjectIterationsFile:

				# TO DO: optimize this logic. What happens if error details are too much to fit into buffer
				list_Error_Iterations_File = fileObjectIterationsFile.readlines()

		else:
			logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file does not exist: " + constants.ERROR_ITERATIONS_FILE)

		if os.path.isfile(constants.ERROR_DETAILS_FILE):
			logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file exists: " + constants.ERROR_DETAILS_FILE)

			# Open this file in read mode
			with open (constants.ERROR_DETAILS_FILE, "r") as fileObjectErrorDetailsFile:

				# TO DO: optimize this logic. What happens if error details are too much to fit into buffer
				list_Error_Details_File = fileObjectErrorDetailsFile.readlines()
				stringError_Details_File = "".join(list_Error_Details_File)

			for line in stringError_Details_File.split('\n'):
				if "FOR PCT TRACKING:" in line:

					# Add this line to append to create summary
					list_For_PCT_Tracking.append (line.split("FOR PCT TRACKING:")[1].strip())

					# Add this line to append to create iteration-wise summary
					# Syntax: some text \t iterationfolder \t some text
					if "\t" in line and line.count ("\t") >= 2:
						list_Error_Iterations_File.append (line.split("\t")[2].strip() + ": " + line.split("\t")[1] + "\n")

			# Count the occurence of each line item which has string "FOR PCT TRACKING:"
			# dict_For_PCT_Tracking = dict((i, list_For_PCT_Tracking.count(i)) for i in list_For_PCT_Tracking)

			# TO DO: optimize this logic. What happens if error details are too much to fit into buffer
			# Remove ": FOR PCT TRACKING: " from string
			list_Error_Iterations_File = list(map(lambda x: x.replace(": FOR PCT TRACKING: ",''),list_Error_Iterations_File))
			
			# TO DO: optimize this logic. What happens if error details are too much to fit into buffer
			# Remove constants.LOG_DIRECTORY_FULL_PATH from path
			list_Error_Iterations_File = list(map(lambda x: x.replace(constants.LOG_DIRECTORY_FULL_PATH + "/",''),list_Error_Iterations_File))

			# Remove duplicates from list
			list_Error_Iterations_File = list (set(list_Error_Iterations_File))

			# Open this file in write mode
			with open (constants.ERROR_ITERATIONS_FILE, "w") as fileObjectIterationsFile:

				# Sort and write content to same file back
				fileObjectIterationsFile.writelines(sorted(list_Error_Iterations_File, key=str.lower))
				logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": after writelines()")

			summary_fail = 0

			# list_Error_Iterations_File has Syntax: string1: string2: string3 : foldername
			# list_Error_Iterations_File_count has syntax: string1: string2: string3
			list_Error_Iterations_File_count = []
			for item in list_Error_Iterations_File:
				if ":" in item:
					list_Error_Iterations_File_count.append( str((":").join(item.split(":")[:-1])))

			# We create dict to show summary of count of occurrence
			dict_File_Difference_Summary = {}
			dict_File_Difference_Summary = dict((x,list_Error_Iterations_File_count.count(x)) for x in set(list_Error_Iterations_File_count))

			# Sort with descending number, reverse the list
			# list_Error_Summary_Reverse_Sorted = sorted(dict_File_Difference_Summary.items(), key=lambda x: x[1], reverse=True)

			# Delete the content for first time. Create error summary file from scratch
			numCountCompleted = 0
			numTargetCount = 0
			with open (constants.ERROR_SUMMARY_FILE, "w") as fileObjectErrorSummaryFile:

				""" Syntax to read: TARGET_COUNT=3 """
				if os.path.isfile(constants.COUNT_TARGET_FILE):
					logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file exists:" + constants.COUNT_TARGET_FILE)
					try:
						with open(constants.COUNT_TARGET_FILE,"r") as fileObjectTargetCount:
							stringTargetCount = fileObjectTargetCount.readline()
							numTargetCount = int(stringTargetCount.split('=')[1])

					except (OSError, IOError) as exception:
						logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

						logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": exiting script")
						exit()

				else:
					logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file does not exist:" + constants.COUNT_TARGET_FILE)

					logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": exiting script")
					exit()

				# Write error summary one-by-one
				# Perform case-insensitive sorting:
				for key in sorted (dict_File_Difference_Summary.keys(), key=str.lower):

					fileObjectErrorSummaryFile.write('%s : %s\n' % (str(dict_File_Difference_Summary[key]), str(key)))

					if "ERROR:" in str(key):
						summary_fail = 1
						# logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": verdict: summary_fail = 1: " + str(key))

					# This count includes original + iterations. Hence, adding one to target count
					if int(dict_File_Difference_Summary[key]) != (int(numTargetCount) +1):
						summary_fail = 1
						logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": verdict: summary_fail = 1: key: " + str(key) + " , numTargetCount: " + str(numTargetCount))

				""" Syntax to read: TARGET_COUNT=3 """
				if os.path.isfile(constants.COUNT_TARGET_FILE):
					try:
						with open(constants.COUNT_TARGET_FILE,"r") as fileObjectTargetCount:
							stringTargetCount = fileObjectTargetCount.readline()
							numTargetCount = int(stringTargetCount.split('=')[1])

					except (OSError, IOError) as exception:
						summary_fail = 1
						logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": verdict: summary_fail = 1: error: " + str(exception))

				else:
					summary_fail = 1
					logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": verdict: summary_fail = 1: file does not exist:" + constants.COUNT_TARGET_FILE)

				""" Syntax to store: CURRENT_COUNT=3 """
				if os.path.isfile(constants.COUNT_COMPLETED_FILE):

					""" Syntax to read: CURRENT_COUNT=3 """
					try:
						with open(constants.COUNT_COMPLETED_FILE,"r+") as fileObjectCountCompleted:
							stringCountCompleted = fileObjectCountCompleted.readline()

						listCountCompleted = stringCountCompleted.split('=')

						if (len(listCountCompleted) == 2):
							numCountCompleted = int(listCountCompleted[1])
						else:
							summary_fail = 1
							logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": verdict: summary_fail = 1: len(listCountCompleted): " + str(len(listCountCompleted)))

					except (OSError, IOError) as exception:
						summary_fail = 1
						logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": verdict: summary_fail = 1: error: " + str(exception))

				else:
					summary_fail = 1
					logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": verdict: summary_fail = 1: file does not exist:" + constants.COUNT_COMPLETED_FILE)

				if (numCountCompleted != numTargetCount):
					fileObjectErrorSummaryFile.write('ERROR: target count != complete count\n')
					summary_fail = 1
					logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": verdict: summary_fail = 1: numTargetCount != numCountCompleted")					

				if summary_fail == 0:
					fileObjectErrorSummaryFile.write('FINAL VERDICT: TEST PASS\n')
				else:
					fileObjectErrorSummaryFile.write('FINAL VERDICT: TEST FAIL\n')

		else:
			logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file does not exist: " + constants.ERROR_DETAILS_FILE)

	except (OSError, IOError, KeyError, json.decoder.JSONDecodeError) as exception:
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": exiting script")
		exit()

	# As part of summary, dump generate_logs also
	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Before calling create_generate_logs_file()")

	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": before generate_logs")
	create_generate_logs_file()

	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": After calling create_generate_logs_file()")
	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Before playing /dev/urandom")

	execute_Command("timeout --signal=KILL 3 aplay /dev/urandom")

	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": After calling timeout --signal=KILL 3 aplay /dev/urandom")

	# store end time
	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Calling sync")
	execute_Command("sync")
	endTime = time.time()

	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Time taken for function execution: " + str(int(endTime-startTime)))

	if int(endTime-startTime) > constants.TIME_FIFTEEN_SECONDS:
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": execution time for " + functionName + " is more than " + str(constants.TIME_FIFTEEN_SECONDS))
		append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + "\t  \t: FOR PCT TRACKING: ERROR: execution time for " + functionName + " is more than " + str(constants.TIME_FIFTEEN_SECONDS) + "\n", os.path.join(constants.LOG_DIRECTORY_FULL_PATH, constants.ERROR_DETAILS_FILE))

def set_corp_proxy(iterationFolderCompletePath):
	"""
	Purpose: Set corp proxy

	Parameters: iterationFolderCompletePath: String: indicates iteration's folder. This includes complete path of iteration

	Returns: None
    """

	""" Create frame object """
	frameObj = currentframe()

	""" String to track current function name """
	functionName = str(frameObj.f_code.co_name) + "()" # Function name

	# store starting time
	startTime = time.time()

	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Entered")

	try:
		# Compare file size only in FF devices
		with open(constants.JSON_CONFIG_FILE_TEST_PARAMETERS) as fileObjectConfigTestParameters:
			dataTestParameters = json.load(fileObjectConfigTestParameters)

			# Iterating through the json dict
			for stringParameter in dataTestParameters:
				# Perform case-insensitive comparison
				if (stringParameter.casefold() == "set_corp_proxy".casefold()):
					if (dataTestParameters[stringParameter].casefold() == "yes".casefold()):
						logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": corp proxy flag is enabled to set proxy " + constants.CORP_PROXY )

						print ("corp proxy is enabled")

						os.environ["http_proxy"] = constants.CORP_PROXY 
						os.environ["HTTP_PROXY"] = constants.CORP_PROXY
						os.environ["https_proxy"] = constants.CORP_PROXY
						os.environ["HTTPS_PROXY"] = constants.CORP_PROXY
					else:
						logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": corp proxy flag is disabled")

		for os_environ_key, os_environ_value in sorted(os.environ.items()):
			logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": os_environ_key: " + os_environ_key + ":" + str(os_environ_value))

	except (OSError, IOError, KeyError, json.decoder.JSONDecodeError, requests.exceptions.Timeout, requests.exceptions.RequestException) as exception:
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

	# store end time
	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Calling sync")
	execute_Command("sync")
	endTime = time.time()

	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Time taken for function execution: " + str(int(endTime-startTime)))

def login_to_DUT(iterationFolderCompletePath):
	"""
	Purpose: Login to DUT using Autotest script

	Parameters: iterationFolderCompletePath: String: indicates iteration's folder. This includes complete path of iteration

	Returns: None
    """

	""" Create frame object """
	frameObj = currentframe()

	""" String to track current function name """
	functionName = str(frameObj.f_code.co_name) + "()" # Function name

	# store starting time
	startTime = time.time()

	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Entered")

	if os.path.isdir(constants.LOGIN_HOME_DIRECTORY):
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": DUT is already logged in")
		return

	try:
		if (os.path.isdir(constants.DESKTOPUI_SIMPLELOGIN_DIRECTORY_USR_LOCAL_PATH) and
			os.path.isfile(constants.DESKTOPUI_SIMPLELOGIN_PY_FILE_SCRIPT_PATH) and
			os.path.isfile(constants.DESKTOPUI_SIMPLELOGIN_CONTROL_FILE_USR_LOCAL_PATH) and
			os.path.isfile(constants.DESKTOPUI_SIMPLELOGIN_PY_FILE_USR_LOCAL_PATH)):

			logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Autotest files are properly present")

			try:
				with open(constants.JSON_CONFIG_FILE_TEST_PARAMETERS) as fileObjectConfigFileTestParameters:
					dataTestParameters = json.load(fileObjectConfigFileTestParameters)

					# Iterating through the json dict
					for stringParameter in dataTestParameters:

						# Perform case-insensitive comparison
						if (stringParameter.casefold() == "login_to_DUT".casefold()):
							if (dataTestParameters[stringParameter].casefold() == "yes".casefold()):
								logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Login to DUT setting is enabled: Before desktopui_SimpleLogin()")

								os.system("/usr/local/autotest/bin/autotest /usr/local/autotest/tests/desktopui_SimpleLogin/control")
								logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Login to DUT setting is enabled: After desktopui_SimpleLogin()")

								# wait for some time after successful login logs to get saved
								time.sleep (constants.TIME_TWO_SECONDS)
							else:
								logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Login to DUT setting is disabled")

			except (OSError, IOError, KeyError, json.decoder.JSONDecodeError) as exception:
				logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

				logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": exiting script")
				exit()

	except (OSError, IOError, json.decoder.JSONDecodeError) as exception:
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": exiting script")
		exit()

	# Print common summary
	if os.path.isdir(constants.LOGIN_HOME_DIRECTORY):
		print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": DUT is logged in")
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": DUT is logged in")
		append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: DUT is logged in\n", os.path.join(constants.LOG_DIRECTORY_FULL_PATH, constants.ERROR_DETAILS_FILE))
	else:
		print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": DUT is NOT logged in")
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": DUT is NOT logged in")
		append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: DUT is NOT logged in\n", os.path.join(constants.LOG_DIRECTORY_FULL_PATH, constants.ERROR_DETAILS_FILE))

	# store end time
	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Calling sync")
	execute_Command("sync")
	endTime = time.time()

	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Time taken for function execution: " + str(int(endTime-startTime)))

	if int(endTime-startTime) > constants.TIME_TWENTY_SECONDS:
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): execution time for " + functionName + " is more than " + str(constants.TIME_TWENTY_SECONDS))
		append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: ERROR: execution time for " + functionName + " is more than " + str(constants.TIME_TWENTY_SECONDS) + "\n", os.path.join(constants.LOG_DIRECTORY_FULL_PATH, constants.ERROR_DETAILS_FILE))
		retain_log_files(iterationFolderCompletePath)

def check_iterations_remaining():
	"""
	Purpose: Check how many iterations are remaining. It will create counter file iterations completed so far

	Parameters: None

	Returns: Integer value of iterations completed
    """

	""" Create frame object """
	frameObj = currentframe()

	""" String to track current function name """
	functionName = str(frameObj.f_code.co_name) + "()" # Function name

	# store starting time
	startTime = time.time()

	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Entered")

	if os.path.isdir(constants.LOG_DIRECTORY_FULL_PATH):
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": directory exists:" + constants.LOG_DIRECTORY_FULL_PATH)
	else:
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": directory does not exist:" + constants.LOG_DIRECTORY_FULL_PATH)
		os.mkdir(constants.LOG_DIRECTORY_FULL_PATH)

	""" Syntax to read: TARGET_COUNT=3 """
	if os.path.isfile(constants.COUNT_TARGET_FILE):
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file exists:" + constants.COUNT_TARGET_FILE)
		try:
			with open(constants.COUNT_TARGET_FILE,"r") as fileObjectTargetCount:

				stringTargetCount = fileObjectTargetCount.readline()
				logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": stringTargetCount: " + stringTargetCount)

				numTargetCount = int(stringTargetCount.split('=')[1])
				logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": numTargetCount: " + str(numTargetCount))

		except (OSError, IOError) as exception:
			logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

			logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": exiting script")
			exit()

	else:
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file does not exist:" + constants.COUNT_TARGET_FILE)

		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": exiting script")
		exit()

	""" Syntax to store: CURRENT_COUNT=3 """
	if os.path.isfile(constants.COUNT_COMPLETED_FILE):
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file exists: " + constants.COUNT_COMPLETED_FILE)

		""" Syntax to read: CURRENT_COUNT=3 """
		try:
			with open(constants.COUNT_COMPLETED_FILE,"r+") as fileObjectCountCompleted:

				stringCountCompleted = fileObjectCountCompleted.readline()

				logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": stringCountCompleted: " + stringCountCompleted)

			listCountCompleted = stringCountCompleted.split('=')

			if (len(listCountCompleted) == 2):
				logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": len(listCountCompleted) == 2")
				numCountCompleted = int(listCountCompleted[1])
			else:
				logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": len(listCountCompleted): " + str(len(listCountCompleted)))

				logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": exiting script")
				exit()

			logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": numCountCompleted: " + str(numCountCompleted))
			logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": numTargetCount: " + str(numTargetCount))

			if (numCountCompleted < numTargetCount):
				logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": numTargetCount < numCountCompleted")

				numCountCompleted = numCountCompleted + 1

				stringCountCompleted = "CURRENT_COUNT=" + str(numCountCompleted)

				logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": numCountCompleted: " + str(numCountCompleted))

				write_string_to_file(stringCountCompleted, constants.COUNT_COMPLETED_FILE)
				logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": write completed: " + constants.COUNT_COMPLETED_FILE)

				# store end time
				logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Calling sync")
				execute_Command("sync")
				endTime = time.time()

				logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Time taken for function execution: " + str(int(endTime-startTime)))

				return numCountCompleted
			else:
				logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": numTargetCount > numCountCompleted")

				""" We remove Autotest script files from location """
				if (os.path.isdir(constants.DESKTOPUI_SIMPLELOGIN_DIRECTORY_USR_LOCAL_PATH)):
					try:
						logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": directory exists: " + constants.DESKTOPUI_SIMPLELOGIN_DIRECTORY_USR_LOCAL_PATH)
						os.remove (constants.DESKTOPUI_SIMPLELOGIN_DIRECTORY_USR_LOCAL_PATH)
					except (OSError, IOError) as exception:
						logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))
				else:
					logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": directory does not exist: " + constants.DESKTOPUI_SIMPLELOGIN_DIRECTORY_USR_LOCAL_PATH)

				logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": removed autotest files")

				""" We remove conf file from /etc/init location """
				if os.path.exists (constants.CONF_FILE_ETC_INIT):
					try:
						logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file exists: " + constants.CONF_FILE_ETC_INIT)
						os.remove (constants.CONF_FILE_ETC_INIT)
					except (OSError, IOError) as exception:
						logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))
				else:
					logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file does not exist: " + constants.CONF_FILE_ETC_INIT)

				logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": removed conf file")

				save_error_summary()
				logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": generated summary file")

				# store end time
				logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Calling sync")
				execute_Command("sync")
				endTime = time.time()

				logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Time taken for function execution: " + str(int(endTime-startTime)))

				""" Tests are finished """
				logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": exiting script: Tests are finished")
				exit()

		except (OSError, IOError) as exception:
			logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

			logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": exiting script")
			exit()
	else:
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file does not exist:" + constants.COUNT_COMPLETED_FILE)

		try:
			""" Open file in write mode """
			stringCountCompleted = "CURRENT_COUNT=1"
			write_string_to_file(stringCountCompleted, constants.COUNT_COMPLETED_FILE)

			logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": stringCountCompleted: " + stringCountCompleted)

		except (OSError, IOError) as exception:
			logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

			logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": exiting script")
			exit()

		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Completed creating file: " + constants.COUNT_COMPLETED_FILE)

		# store end time
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Calling sync")
		execute_Command("sync")
		endTime = time.time()

		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Time taken for function execution: " + str(int(endTime-startTime)))

		# This is first iteration and starts with 1
		return 1

def create_generate_logs_file():
	"""
	Purpose: Ensure that Autotest scripts are copied to allow automatic login.
	If autotest scripts are NOT copied correctly, it prompts user about it and exits the script.
	This stops any further test execution.

	Parameters: None

	Returns: None
    """

	""" Create frame object """
	frameObj = currentframe()

	""" String to track current function name """
	functionName = str(frameObj.f_code.co_name) + "()" # Function name

	# store starting time
	startTime = time.time()

	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Entered")

	# generate_logs is executed only if dmp files are less
	total_number_of_dump_files = 0
	for root, dirs, files in os.walk(constants.LOG_DIRECTORY_FULL_PATH):
		for file in files:
			if file.endswith(".dmp"):
				logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": found dump file: " + os.path.join(root, file))
				total_number_of_dump_files = total_number_of_dump_files + 1

	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": total_number_of_dump_files: " + str(total_number_of_dump_files))

	# generate_logs is executed only if dmp files are less
	if (total_number_of_dump_files <= constants.NUMBER_OF_DUMP_FILES_TOLERANCE_VALUE):
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Before generate_logs")

		execute_Command("generate_logs --output=" + constants.LOG_DIRECTORY_FULL_PATH + "/generate_logs.tgz")

		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": After generate_logs")

		fileSize_generate_logs = os.path.getsize(os.path.join(constants.LOG_DIRECTORY_FULL_PATH, "generate_logs.tgz"))

		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": fileSize_generate_logs: " + str(fileSize_generate_logs))

		if (fileSize_generate_logs > constants.TWO_HUNDRED_MB):
			logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file size is more, removing generate_logs file")
			os.remove (os.path.join(constants.LOG_DIRECTORY_FULL_PATH, "generate_logs.tgz"))

	# store end time
	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Calling sync")
	execute_Command("sync")
	endTime = time.time()

	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Time taken for function execution: " + str(int(endTime-startTime)))

	if int(endTime-startTime) > constants.TIME_FIFTEEN_SECONDS:
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): execution time for " + functionName + " is more than " + str(constants.TIME_FIFTEEN_SECONDS))
		append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + "\t create_generate_logs_file() \t: FOR PCT TRACKING: ERROR: execution time for " + functionName + " is more than " + str(constants.TIME_FIFTEEN_SECONDS) + "\n", os.path.join(constants.LOG_DIRECTORY_FULL_PATH, constants.ERROR_DETAILS_FILE))
		# retain_log_files(iterationFolderCompletePath)

def copy_autotest_files():
	"""
	Purpose: Ensure that Autotest scripts are copied to allow automatic login.
	If autotest scripts are NOT copied correctly, it prompts user about it and exits the script.
	This stops any further test execution.

	Parameters: None

	Returns: None
    """

	""" Create frame object """
	frameObj = currentframe()

	""" String to track current function name """
	functionName = str(frameObj.f_code.co_name) + "()" # Function name

	# store starting time
	startTime = time.time()

	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Entered")

	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": sourceDirectory: " + constants.DESKTOPUI_SIMPLELOGIN_DIRECTORY_SCRIPT_PATH)
	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": destinationDirectory: " + constants.DESKTOPUI_SIMPLELOGIN_DIRECTORY_USR_LOCAL_PATH)

	if os.path.isdir(constants.DESKTOPUI_SIMPLELOGIN_DIRECTORY_SCRIPT_PATH):
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": source directory exists: " + constants.DESKTOPUI_SIMPLELOGIN_DIRECTORY_SCRIPT_PATH)
	else:
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": source directory does not exist: " + constants.DESKTOPUI_SIMPLELOGIN_DIRECTORY_SCRIPT_PATH)
		print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": ERROR: source directory does not exist: " + constants.DESKTOPUI_SIMPLELOGIN_DIRECTORY_SCRIPT_PATH)

		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": exiting script")
		exit()

	try:
		# Remove older content
		if os.path.isdir(constants.DESKTOPUI_SIMPLELOGIN_DIRECTORY_USR_LOCAL_PATH):
			logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": directory exists: " + constants.DESKTOPUI_SIMPLELOGIN_DIRECTORY_USR_LOCAL_PATH)

			# Remove
			shutil.rmtree(constants.DESKTOPUI_SIMPLELOGIN_DIRECTORY_USR_LOCAL_PATH)
			logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": after deleting directory: " + constants.DESKTOPUI_SIMPLELOGIN_DIRECTORY_USR_LOCAL_PATH)

			# Remove older content
			if os.path.isdir(constants.DESKTOPUI_SIMPLELOGIN_DIRECTORY_USR_LOCAL_PATH):
				logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": directory exists: " + constants.DESKTOPUI_SIMPLELOGIN_DIRECTORY_USR_LOCAL_PATH)
				exit()
			else:
				logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": directory deleted successfully: " + constants.DESKTOPUI_SIMPLELOGIN_DIRECTORY_USR_LOCAL_PATH)

		else:
			logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": directory does not exist: " + constants.DESKTOPUI_SIMPLELOGIN_DIRECTORY_USR_LOCAL_PATH)

	except (OSError, IOError) as exception:
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

	try:
		shutil.copytree (constants.DESKTOPUI_SIMPLELOGIN_DIRECTORY_SCRIPT_PATH, constants.DESKTOPUI_SIMPLELOGIN_DIRECTORY_USR_LOCAL_PATH)
	except FileNotFoundError:
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": FileNotFoundError: " + str(FileNotFoundError))

	# Give some delay for file operation to reflect that files are copied
	time.sleep (constants.TIME_ONE_SECOND)

	if os.path.isfile(constants.DESKTOPUI_SIMPLELOGIN_CONTROL_FILE_USR_LOCAL_PATH):
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file exists: " + constants.DESKTOPUI_SIMPLELOGIN_CONTROL_FILE_USR_LOCAL_PATH)
	else:
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file does not exist: " + constants.DESKTOPUI_SIMPLELOGIN_CONTROL_FILE_USR_LOCAL_PATH)
		print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": ERROR: file does not exist: " + constants.DESKTOPUI_SIMPLELOGIN_CONTROL_FILE_USR_LOCAL_PATH)
		exit()			

	if os.path.isfile(constants.DESKTOPUI_SIMPLELOGIN_PY_FILE_USR_LOCAL_PATH):
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file exists: " + constants.DESKTOPUI_SIMPLELOGIN_PY_FILE_USR_LOCAL_PATH)
	else:
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file does not exist: " + constants.DESKTOPUI_SIMPLELOGIN_PY_FILE_USR_LOCAL_PATH)
		print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": ERROR: file does not exist: " + constants.DESKTOPUI_SIMPLELOGIN_PY_FILE_USR_LOCAL_PATH)
		exit()

	# store end time
	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Calling sync")
	execute_Command("sync")
	endTime = time.time()

	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Time taken for function execution: " + str(int(endTime-startTime)))

def write_target_count(argumentNumberOfIterations):
	"""
	Purpose: Copy target count of test to file

	Parameters: int: value to write ass target count of test

	Returns: None
	"""

	""" Create frame object """
	frameObj = currentframe()

	""" String to track current function name """
	functionName = str(frameObj.f_code.co_name) + "()" # Function name

	# store starting time
	startTime = time.time()

	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Entered")

	if os.path.isfile(constants.COUNT_TARGET_FILE):
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file exists: " + constants.COUNT_TARGET_FILE)
		os.remove(constants.COUNT_TARGET_FILE)
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": after removing file: " + constants.COUNT_TARGET_FILE)
	else:
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file does not exists: " + constants.COUNT_TARGET_FILE)

	""" Syntax to store: TARGET_COUNT=3 """
	try:
		with open(constants.COUNT_TARGET_FILE,"w") as fileObjectTargetCount:
			stringTargetCount = "TARGET_COUNT=" + str(argumentNumberOfIterations)
			fileObjectTargetCount.write(stringTargetCount)

			logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": stringTargetCount: " + stringTargetCount)

	except (OSError, IOError) as exception:
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))


	if os.path.isfile(constants.COUNT_TARGET_FILE):
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file exists: " + constants.COUNT_TARGET_FILE)
	else:
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file does not exist: " + constants.COUNT_TARGET_FILE)
		exit()

	# store end time
	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Calling sync")
	execute_Command("sync")
	endTime = time.time()

	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Time taken for function execution: " + str(int(endTime-startTime)))

def write_CONF_FILE_ETC_INIT(confString):
	"""
	Purpose: Copy target count of test to file

	Parameters: int value to write ass target count of test

	Returns: None
	"""

	""" Create frame object """
	frameObj = currentframe()

	""" String to track current function name """
	functionName = str(frameObj.f_code.co_name) + "()" # Function name

	# store starting time
	startTime = time.time()

	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Entered")

	if os.path.isfile(constants.CONF_FILE_ETC_INIT):
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file exists: " + constants.CONF_FILE_ETC_INIT)
		os.remove(constants.CONF_FILE_ETC_INIT)
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": after removing file: " + constants.CONF_FILE_ETC_INIT)
	else:
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file does not exist: " + constants.CONF_FILE_ETC_INIT)

	""" Syntax to store: TARGET_COUNT=3 """
	try:
		with open(constants.CONF_FILE_ETC_INIT,"w") as fileObjectConfFileEtcInit:
			fileObjectConfFileEtcInit.write(confString)

			logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": confString: " + confString)

		time.sleep (constants.TIME_TWO_SECONDS)
	except (OSError, IOError) as exception:
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))
		print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": error:" + str(exception))
		exit()


	if os.path.isfile(constants.CONF_FILE_ETC_INIT):
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file exists: " + constants.CONF_FILE_ETC_INIT)
	else:
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file does not exist: " + constants.CONF_FILE_ETC_INIT)
		exit()

	# store end time
	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Calling sync")
	execute_Command("sync")
	endTime = time.time()

	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Time taken for function execution: " + str(int(endTime-startTime)))

def cleanup_old_files():
	"""
	Purpose: Clean older logs from tool and older dump files

	Parameters: None

	Returns: None
    """

	""" Create frame object """
	frameObj = currentframe()

	""" String to track current function name """
	functionName = str(frameObj.f_code.co_name) + "()" # Function name

	# store starting time
	startTime = time.time()

	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Entered")

	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": Entered")
	try:
		# os.remove (constants.LOG_DIRECTORY_FULL_PATH)
		# Create zip file of earlier logs
		print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": before make_archive")
		nowTimeDate = datetime.datetime.now()
		
		# Get size of folder, before we zip it
		forZip_size = 0
		for forZip_path, forZip_dirs, forZip_files in os.walk(constants.LOG_DIRECTORY_FULL_PATH):
			for forZip_fileName in forZip_files:
				forZip_filepath = os.path.join(forZip_path, forZip_fileName)
				forZip_size += os.path.getsize(forZip_filepath)

			# if folder size is more, then no need to walk-thorough all folders/files
			if forZip_size >= constants.ONE_MB:
				print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": Breaking for loop, folder size is more than 1MB: " + str(forZip_size))
				break
 
		if forZip_size >= constants.ONE_MB:
			print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": Zipping folder, folder size is more than 1MB: " + str(forZip_size))

			test_operation = ""
			if os.path.isfile(constants.STRING_TEST_OPERATION_FILE):
				try:
					with open(constants.STRING_TEST_OPERATION_FILE,"r") as fileObjectTestOperation:

						test_operation = str(fileObjectTestOperation.readline()) + "_"
						logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": test_operation: " + test_operation)

				except (OSError, IOError) as exception:
					logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))
					exit()

			zipFileName = "pct_logs_" + test_operation + str(nowTimeDate.strftime("%d%m%Y_%H%M%S"))
			print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": zipFileName: " + zipFileName)
			shutil.make_archive(os.path.join("/usr/local", zipFileName), "zip", constants.LOG_DIRECTORY_FULL_PATH)
			print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": after make_archive")
		else:
			print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": Not zipping folder, folder size is less than 1MB: " + str(forZip_size))

		shutil.rmtree(constants.LOG_DIRECTORY_FULL_PATH)
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": after remove dir")
		os.mkdir(constants.LOG_DIRECTORY_FULL_PATH)
	except (OSError, IOError) as exception:
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

	if os.path.isdir(constants.LOG_DIRECTORY_FULL_PATH):
		print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": directory exists: " + constants.LOG_DIRECTORY_FULL_PATH)
	else:
		try:
			print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": directory does not exist: " + constants.LOG_DIRECTORY_FULL_PATH)
			os.mkdir(constants.LOG_DIRECTORY_FULL_PATH)
			print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": directory created: " + constants.LOG_DIRECTORY_FULL_PATH)
		except (FileNotFoundError,OSError, IOError) as exception:
			print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))
			exit()

	# store end time
	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Calling sync")
	execute_Command("sync")
	endTime = time.time()

	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Time taken for function execution: " + str(int(endTime-startTime)))

def show_Help():
	"""
	Purpose: Clean older logs from tool and older dump files

	Parameters: None

	Returns: None
    """

	""" Create frame object """
	frameObj = currentframe()

	""" String to track current function name """
	functionName = str(frameObj.f_code.co_name) + "()" # Function name

	# store starting time
	startTime = time.time()

	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Entered")

	print (
	'''Syntax is: python start_tests.py <TestNumber> <NumberOfIterations>
	where both <TestNumber> and <NumberOfIterations> must be positive integers

	TestNumber is any number from 1-13:
	1) Disable ssd root verification. Do not pass any other parameter
	2) Capture logs for original
	3) Run Cold Boot Test from S5. Pass parameter for number of iterations.
	4) Run Cold Boot Test from G3. Pass parameter for number of iterations.
	5) Run Cold Boot Quick Test (S0-S5). Pass parameter for number of iterations.
	6) Run Cold Boot Quick Test (S0-S5-G3). Pass parameter for number of iterations.
	7) Run Warm Boot Test. Pass parameter for number of iterations.
	8) Run Warm Boot Quick Test. Pass parameter for number of iterations.
	9) Run Suspend-Resume Stress test for S0ix. Pass parameter for number of iterations.
	10) Run Cold Boot Quick Test (S0-S5) + suspend-resume quick test. Pass parameter for number of iterations for cold boot
	11) Run Cold Boot Quick Test (S0-S5-G3) + suspend-resume quick test. Pass parameter for number of iterations for cold boot
	12) Run Warm Boot Quick Test + suspend-resume quick test. Pass parameter for number of iterations for warm boot
	13) Run Cold Boot Quick Test (S0-S5-G3) + warm boot quick test. Pass parameter for total number of iterations(warm + cold)

	<NumberOfIterations> is any number between 3 and 10000
	''')
	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Exiting")

	# store end time
	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Calling sync")
	execute_Command("sync")
	endTime = time.time()

	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Time taken for function execution: " + str(int(endTime-startTime)))

def ensure_rootfs_verification_disabled():
	"""
	Purpose: Ensure rootfs verification is disabled.
	If rootfs verificaition is not enabled, it prompts user to disable it and exits the script.
	This stops any further test execution.

	Parameters: None

	Returns: None
    """

	""" Create frame object """
	frameObj = currentframe()

	""" String to track current function name """
	functionName = str(frameObj.f_code.co_name) + "()" # Function name

	# store starting time
	startTime = time.time()

	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Entered")

	rootfs_verification_ro_rw = execute_Command("cat /proc/mounts | grep '/dev/root' | cut -d ' ' -f4 | cut -d ',' -f1")
	if "rw" in rootfs_verification_ro_rw:
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": rootfs verification is disabled in /proc/mounts: " + rootfs_verification_ro_rw)
	else:
		print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": rootfs verification is NOT disabled in /proc/mounts: " + rootfs_verification_ro_rw)
		print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": exiting script")

		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": rootfs verification is NOT disabled in /proc/mounts: " + rootfs_verification_ro_rw)
		exit()

	rootfs_verification_rootdev = execute_Command("rootdev")
	if "/dev/dm" in rootfs_verification_rootdev:
		print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": rootfs verification is NOT disabled in rootdev check for /dev/dm: " + rootfs_verification_rootdev)
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": rootfs verification is NOT disabled in rootdev check for /dev/dm: " + rootfs_verification_rootdev)
	else:
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": rootfs verification is disabled in rootdev check for /dev/dm: " + rootfs_verification_rootdev)
	
	if "/dev/sd" in rootfs_verification_rootdev:
		print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": rootfs verification is NOT disabled in rootdev check for /dev/sd: " + rootfs_verification_rootdev)
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": rootfs verification is NOT disabled in rootdev check for /dev/sd: " + rootfs_verification_rootdev)
	else:
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": rootfs verification is disabled in rootdev check for /dev/sd: " + rootfs_verification_rootdev)

	try:
		with open(constants.CONF_FILE_ETC_INIT, 'wb') as fileObjectConfigEtcInit:
			num_chars = 1024 * 1024
			fileObjectConfigEtcInit.write(os.urandom(num_chars))

		if os.path.exists (constants.CONF_FILE_ETC_INIT):
			try:
				logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file exists: " + constants.CONF_FILE_ETC_INIT)
				os.remove (constants.CONF_FILE_ETC_INIT)
				print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": /etc/init is RW")
				logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": /etc/init is RW")
			except (OSError, IOError) as exception:
				logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))
				exit()
	except (OSError, IOError) as exception:
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))
		exit()

	# store end time
	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Calling sync")
	execute_Command("sync")
	endTime = time.time()

	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Time taken for function execution: " + str(int(endTime-startTime)))

def clear_elogtool_log():
	"""
	Purpose: clear old elogtool logs.

	Parameters: None

	Returns: None
    """

	""" Create frame object """
	frameObj = currentframe()

	""" String to track current function name """
	functionName = str(frameObj.f_code.co_name) + "()" # Function name

	# store starting time
	startTime = time.time()

	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Entered")

	execute_Command("elogtool clear")

	# store end time
	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Calling sync")
	execute_Command("sync")
	endTime = time.time()

	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Time taken for function execution: " + str(int(endTime-startTime)))

def start_shutdown_reboot_counter(stringFolderName_NowTimeDate, sleepTime):
	"""
	Purpose: Ensure that DUT is connected to network (at least one of Ethernet, Wi-Fi, WWAN).
	If network is not connected, it prompts user to connect to network and exits the script.
	This stops any further test execution.

	Parameters: None

	Returns: None
    """

	""" Create frame object """
	frameObj = currentframe()

	""" String to track current function name """
	functionName = str(frameObj.f_code.co_name) + "()" # Function name

	# store starting time
	startTime = time.time()

	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Entered function: folder name: " + stringFolderName_NowTimeDate + " : sleepTime (seconds): " + str(sleepTime))

	intCounter = int(sleepTime)
	time.sleep (intCounter)

	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): after sleep of " + str(sleepTime))
	append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + " :\t" + stringFolderName_NowTimeDate + "\t: FOR PCT TRACKING: ERROR: reboot/shutdown time is more than " + str(sleepTime) + "seconds\n", constants.ERROR_DETAILS_FILE)
	retain_log_files(iterationFolderCompletePath)

	while intCounter <= constants.TEN_MINUTES_IN_SECONDS:
		intCounter = intCounter + 1
		time.sleep (constants.TIME_TWO_SECONDS)

		if (intCounter % 2 == 0):
			logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + " : " + stringFolderName_NowTimeDate + ": time after reboot/shutdown (seconds): " + str(intCounter))

	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + " : " + stringFolderName_NowTimeDate + ": reboot/shutdown operation took more than seconds: " + str(constants.TEN_MINUTES_IN_SECONDS))
	exit()

def move_var_log_messages_folder(iterationFolderCompletePath):
	"""
	Purpose: Copy /var/log/messages file to folder

	Parameters: iterationFolderCompletePath: String: indicates iteration's folder. This includes complete path of iteration

	Returns: None
    """

	""" Create frame object """
	frameObj = currentframe()

	""" String to track current function name """
	functionName = str(frameObj.f_code.co_name) + "()" # Function name

	# store starting time
	startTime = time.time()

	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Entered")

	try:

		# Compare file size only in FF devices
		with open(constants.JSON_CONFIG_FILE_TEST_PARAMETERS) as fileObjectConfigTestParameters:
			dataTestParameters = json.load(fileObjectConfigTestParameters)

			# Iterating through the json dict
			for stringParameter in dataTestParameters:
				# Perform case-insensitive comparison
				if (stringParameter.casefold() == "move_var_log_messages_folder".casefold()):
					if (dataTestParameters[stringParameter].casefold() == "yes".casefold()):
						logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": move_var_log_messages_folder is enabled")

						if os.path.isfile(constants.VAR_LOG_MESSAGES_FULL_PATH):
							logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file exists: " + constants.VAR_LOG_MESSAGES_FULL_PATH)

							shutil.move(constants.VAR_LOG_MESSAGES_FULL_PATH, iterationFolderCompletePath)

							logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": after move operation")

	except (OSError, IOError, KeyError, json.decoder.JSONDecodeError, requests.exceptions.Timeout, requests.exceptions.RequestException) as exception:
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): error: " + str(exception))
		append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: ERROR: move var log messages folder is not initiated\n", os.path.join(constants.LOG_DIRECTORY_FULL_PATH, constants.ERROR_DETAILS_FILE))
		retain_log_files(iterationFolderCompletePath)

	# store end time
	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Calling sync")
	execute_Command("sync")
	endTime = time.time()

	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Time taken for function execution: " + str(int(endTime-startTime)))

def clear_net_log(iterationFolderCompletePath = "default"):
	"""
	Purpose: Clear /var/log/net.log file

	Parameters: iterationFolderCompletePath: String: indicates iteration's folder. This includes complete path of iteration

	Returns: None
    """

	""" Create frame object """
	frameObj = currentframe()

	""" String to track current function name """
	functionName = str(frameObj.f_code.co_name) + "()" # Function name

	# store starting time
	startTime = time.time()

	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Entered")

	if os.path.exists ("/var/log/net.log"):
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": log file exists: /var/log/net.log")
		execute_Command("echo "" > /var/log/net.log")
	else:
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): file /var/log/net.log does not exist")
		append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: ERROR: file /var/log/net.log does not exist\n", os.path.join(constants.LOG_DIRECTORY_FULL_PATH, constants.ERROR_DETAILS_FILE))
		retain_log_files(iterationFolderCompletePath)

	# store end time
	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Calling sync")
	execute_Command("sync")
	endTime = time.time()

	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Time taken for function execution: " + str(int(endTime-startTime)))

def clear_typecd_log(iterationFolderCompletePath = "default"):
	"""
	Purpose: Clear /var/log/typecd.log file

	Parameters: iterationFolderCompletePath: String: indicates iteration's folder This includes complete path of iteration

	Returns: None
    """

	""" Create frame object """
	frameObj = currentframe()

	""" String to track current function name """
	functionName = str(frameObj.f_code.co_name) + "()" # Function name

	# store starting time
	startTime = time.time()

	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Entered")

	if os.path.exists ("/var/log/typecd.log"):
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": log file exists: /var/log/typecd.log")
		os.remove("/var/log/typecd.log")
	else:
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): file /var/log/typecd.log does not exist")
		append_String_To_File(iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: ERROR: file /var/log/typecd.log does not exist\n", os.path.join(constants.LOG_DIRECTORY_FULL_PATH, constants.ERROR_DETAILS_FILE))
		retain_log_files(iterationFolderCompletePath)

	# store end time
	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Calling sync")
	execute_Command("sync")
	endTime = time.time()

	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Time taken for function execution: " + str(int(endTime-startTime)))

def measure_bootperf(iterationFolderCompletePath):
	"""
	Purpose: Measure boot time performance

	Parameters: iterationFolderCompletePath: String: indicates iteration's folder. This includes complete path of iteration

	Returns: None
    """

	""" Create frame object """
	frameObj = currentframe()

	""" String to track current function name """
	functionName = str(frameObj.f_code.co_name) + "()" # Function name

	# store starting time
	startTime = time.time()
	
	# seconds_power_on_to_kernel=$(cat /tmp/firmware-boot-time | head -1)
	# seconds_kernel_to_login=$(cat /tmp/uptime-login-prompt-visible |awk '{print $1}' | head -1)
	# seconds_power_on_to_login=$(echo $seconds_power_on_to_kernel $seconds_kernel_to_login |awk '{print $1 + $2}')

	seconds_power_on_to_kernel = 0
	seconds_kernel_to_login = 0
	seconds_power_on_to_login = 0

	try:
		if os.path.isfile(constants.FIRMWARE_BOOT_TIME):
			logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file exists: " + constants.FIRMWARE_BOOT_TIME)

			# Open this file in read mode now
			with open (constants.FIRMWARE_BOOT_TIME, "r") as fileObjectFirmwareBootTime:
				# Read only the first line
				seconds_power_on_to_kernel = float(fileObjectFirmwareBootTime.readline().rstrip())
				logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": seconds_power_on_to_kernel: " + str(seconds_power_on_to_kernel))

				if (seconds_power_on_to_kernel <= 0):
					logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): seconds_power_on_to_kernel is less than 0")
					append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: ERROR: seconds_power_on_to_kernel is less than or equal to 0\n", os.path.join(constants.LOG_DIRECTORY_FULL_PATH, constants.ERROR_DETAILS_FILE))
					retain_log_files(iterationFolderCompletePath)
					return

		else:
			logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): file does not exists: " + constants.FIRMWARE_BOOT_TIME)
			append_String_To_File(iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: ERROR: file does not exists: " + constants.FIRMWARE_BOOT_TIME + "\n", os.path.join(constants.LOG_DIRECTORY_FULL_PATH, constants.ERROR_DETAILS_FILE))
			retain_log_files(iterationFolderCompletePath)
			return

		if os.path.isfile(constants.UPTIME_LOGIN_PROMPT_VISIBLE):
			logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file exists: " + constants.UPTIME_LOGIN_PROMPT_VISIBLE)

			# Open this file in read mode now
			with open (constants.UPTIME_LOGIN_PROMPT_VISIBLE, "r") as fileObjectUptimeLoginPromtVisible:
				# Read only the first line
				seconds_kernel_to_login = float(fileObjectUptimeLoginPromtVisible.readline().rstrip())
				logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": seconds_kernel_to_login: " + str(seconds_kernel_to_login))

				if (seconds_kernel_to_login <= 0):
					logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): seconds_kernel_to_login is less than 0")
					append_String_To_File(fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: ERROR: seconds_kernel_to_login is less than or equal to 0\n", os.path.join(constants.LOG_DIRECTORY_FULL_PATH, constants.ERROR_DETAILS_FILE))
					retain_log_files(iterationFolderCompletePath)
					return

		else:
			logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): file does not exists: " + constants.UPTIME_LOGIN_PROMPT_VISIBLE)
			append_String_To_File(iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: ERROR: file does not exists: " + constants.UPTIME_LOGIN_PROMPT_VISIBLE + "\n", os.path.join(constants.LOG_DIRECTORY_FULL_PATH, constants.ERROR_DETAILS_FILE))
			retain_log_files(iterationFolderCompletePath)
			return

		seconds_power_on_to_login = seconds_power_on_to_kernel + seconds_kernel_to_login

		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": seconds_power_on_to_login is : " + str(seconds_power_on_to_login))

		# Check if normal mode or developer mode
		expectedValue_seconds_power_on_to_login = 0
		crossystem_mainfwTypeString = execute_Command("crossystem | grep mainfw_type")

		if "developer" in crossystem_mainfwTypeString:
			expectedValue_seconds_power_on_to_login = constants.TARGET_SECONDS_POWER_ON_TO_LOGIN_DEVELOPER_MODE #12.5

		if "normal" in crossystem_mainfwTypeString:
			expectedValue_seconds_power_on_to_login = constants.TARGET_SECONDS_POWER_ON_TO_LOGIN_NORMAL_MODE #8.5

		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": expectedValue_seconds_power_on_to_login : " + str(expectedValue_seconds_power_on_to_login))

		if (seconds_power_on_to_login >= expectedValue_seconds_power_on_to_login):
			logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): seconds_power_on_to_login is more than expected")
			append_String_To_File(iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: ERROR: seconds_power_on_to_login is more than expected\n", os.path.join(constants.LOG_DIRECTORY_FULL_PATH, constants.ERROR_DETAILS_FILE))
			retain_log_files(iterationFolderCompletePath)

			with open(constants.JSON_CONFIG_FILE_TEST_PARAMETERS) as fileObjectConfigFileTestParameters:
				dataTestParameters = json.load(fileObjectConfigFileTestParameters)

				# Iterating through the json dict
				for stringParameter in dataTestParameters:

					# Perform case-insensitive comparison
					if (stringParameter.casefold() == "stop_on_error_boot_perf".casefold()):
						if (dataTestParameters[stringParameter].casefold() == "yes".casefold()):
							logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": before writing file for stop_on_error for: " + stringParameter)

							with open(constants.STOP_ON_ERROR_FILE,"w") as fileObjectStopOnError:
								fileObjectStopOnError.write (str("STOP_ON_ERROR"))
								

							logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": after writing files for stop_on_error")

						else:
							logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": stop_on_error for network connection is NOT enabled")


	except (OSError, IOError, KeyError, json.decoder.JSONDecodeError) as exception:
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))
		exit()

	# store end time
	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Calling sync")
	execute_Command("sync")
	endTime = time.time()

	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Time taken for function execution: " + str(int(endTime-startTime)))

def parse_bootstat_Summary(iterationFolderCompletePath):
	"""
	Purpose: Parse output of bootstat_summary file

	Parameters: iterationFolderCompletePath: String: indicates iteration's folder which contains bootstat_summary log file. This includes complete path of iteration

	Returns: None
    """

	""" Create frame object """
	frameObj = currentframe()

	""" String to track current function name """
	functionName = str(frameObj.f_code.co_name) + "()" # Function name

	# store starting time
	startTime = time.time()

	bootstat_SummaryFileNameWithCompletePath = os.path.join(iterationFolderCompletePath, "boot_summary_original.txt")

	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Entered")

	if os.path.isfile(bootstat_SummaryFileNameWithCompletePath):
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file exists: " + bootstat_SummaryFileNameWithCompletePath)
	else:
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): file does not exists: " + bootstat_SummaryFileNameWithCompletePath)
		append_String_To_File(iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: ERROR: file does not exists: " + bootstat_SummaryFileNameWithCompletePath + "\n", os.path.join(constants.LOG_DIRECTORY_FULL_PATH, constants.ERROR_DETAILS_FILE))
		retain_log_files(iterationFolderCompletePath)
		return

	if os.path.isfile(constants.JSON_CONFIG_FILE_ERROR_STRINGS):
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file exists: " + constants.JSON_CONFIG_FILE_ERROR_STRINGS)
	else:
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file does not exist: " + constants.JSON_CONFIG_FILE_ERROR_STRINGS)
		return

	try:
		with open(bootstat_SummaryFileNameWithCompletePath, 'r') as fileObjectBootstatSummary:
			list_bootstatSummary = fileObjectBootstatSummary.readlines()

		dict_bootStatSummaryEvent_ObservedValue = {}

		# Remove first item from bootstat_Summary, if it is header
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": length of list_bootstatSummary: " + str(len(list_bootstatSummary)))
		if any ("time %cpu       dt  %dt  event" in listItem for listItem in list_bootstatSummary):
			list_bootstatSummary.pop(0)
			logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": popping up time cpu dt t event")

		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": length of list_bootstatSummary: " + str(len(list_bootstatSummary)))

		for line_bootStatSummary in list_bootstatSummary:
			list_bootstatSummaryEvent_ObservedTime = line_bootStatSummary.split()

			if (list_bootstatSummaryEvent_ObservedTime[0].isdigit()):
				# Ensure that only first key-value pair is added
				# Check if key is present in dict
				if str(list_bootstatSummaryEvent_ObservedTime[4]) not in dict_bootStatSummaryEvent_ObservedValue:
					dict_bootStatSummaryEvent_ObservedValue[ str(list_bootstatSummaryEvent_ObservedTime[4]) ] = list_bootstatSummaryEvent_ObservedTime[0]
			else:
				logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": calling retain_log_files(): string is not number in bootstatSummary for: " + str(list_bootstatSummaryEvent_ObservedTime[4]))
				append_String_To_File(iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ":\t" + iterationFolderCompletePath + "\t: FOR PCT TRACKING: ERROR: string is not number in bootstatSummary for: " + str(list_bootstatSummaryEvent_ObservedTime[4]) + "\n", os.path.join(constants.LOG_DIRECTORY_FULL_PATH, constants.ERROR_DETAILS_FILE))
				retain_log_files(iterationFolderCompletePath)

		# Iterating through the json file. it is dict of dict
		with open(constants.JSON_CONFIG_FILE_COMPARE_LOGS) as fileObjectConfigFileCompareLogs:
			dataBootStatSummaryString = json.load(fileObjectConfigFileCompareLogs)

			# Iterating through the json file. It is dict
			for bootstatSummaryEventString, stopOnErrorString_expectedValueString in dataBootStatSummaryString['parse_bootstat_summary'].items():
				stopOnErrorString = stopOnErrorString_expectedValueString[0]
				expectedValue = int(stopOnErrorString_expectedValueString[1])

				if bootstatSummaryEventString in dict_bootStatSummaryEvent_ObservedValue.keys():
					if int(dict_bootStatSummaryEvent_ObservedValue[bootstatSummaryEventString]) <= expectedValue:
						logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": value within tolerance for: " + bootstatSummaryEventString)
					else:
						logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": value not within tolerance for: " + bootstatSummaryEventString)

						# Perform case-insensitive comparison
						if (stopOnErrorString.casefold() != "STOP_ON_ERROR_NO".casefold()):
							logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": before writing file for stop_on_error for: " + bootstatSummaryEventString)

							try:
								with open(constants.STOP_ON_ERROR_FILE,"w") as fileObjectStopOnError:
									fileObjectStopOnError.write (str("STOP_ON_ERROR"))

							except (OSError, IOError) as exception:
								logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

							logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": after writing files for stop_on_error for " + bootstatSummaryEventString)

						else:
							logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": stop_on_error is NOT enabled for " + bootstatSummaryEventString)

				else:
					logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": value not found in bootstatSummary for: " + bootstatSummaryEventString)

	except (OSError, IOError, KeyError, json.decoder.JSONDecodeError) as exception:
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))
		exit()

	# store end time
	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Calling sync")
	execute_Command("sync")
	endTime = time.time()

	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Time taken for function execution: " + str(int(endTime-startTime)))

def ensure_network_connection(iterationFolderCompletePath = "original"):
	"""
	Purpose: Ensure that DUT is connected to network (at least one of Ethernet, Wi-Fi, WWAN).
	If network is not connected, it prompts user to connect to network and exits the script.
	This stops any further test execution.

	Parameters: None

	Returns: None
    """

	""" Create frame object """
	frameObj = currentframe()

	""" String to track current function name """
	functionName = str(frameObj.f_code.co_name) + "()" # Function name

	# store starting time
	startTime = time.time()

	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Entered")

	retryCount = 0

	while retryCount < constants.IP_ADDRESS_RETRY_ATTEMPTS:
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": retryCount: " + str(retryCount))

		if (retryCount != 0):
			print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": ensure_network_connection retryCount: " + str(retryCount))

		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Before calling sync")
		execute_Command("sync")
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": After calling sync")

		ip_o_addr_list = execute_Command("ip -o -4 addr list")

		# Changed sequence of network interfaces to allow sync
		eth1_ip=0
		eth1_connected = execute_Command("ifconfig -a | grep '^eth1' | wc -c")
		if (int(eth1_connected) == 0):
			logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": eth1 is not present")
		else:
			# print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": eth1 is present")
			eth1_ip = execute_Command("ip -o -4 addr list eth1 | awk '{print $4}' | cut -d/ -f1 | wc -w")
			if (int(eth1_ip) != 0):
				# print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": eth1 is connected")
				logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": eth1 is connected: ")
			else:
				logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": eth1 is NOT connected: " + ip_o_addr_list)

		eth0_ip=0
		eth0_connected = execute_Command("ifconfig -a | grep '^eth0' | wc -c")
		if (int(eth0_connected) == 0):
			logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": eth0 is not present")
		else:
			# print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": eth0 is present")
			eth0_ip = execute_Command("ip -o -4 addr list eth0 | awk '{print $4}' | cut -d/ -f1 | wc -w")
			if (int(eth0_ip) != 0):
				# print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": eth0 is connected")
				logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": eth0 is connected: ")
			else:
				logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": eth0 is NOT connected: " + ip_o_addr_list)

		ccmni0_ip=0
		ccmni0_connected = execute_Command("ifconfig -a | grep '^ccmni0' | wc -c")
		if (int(ccmni0_connected) == 0):
			logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": ccmni0 is not present")
		else:
			# print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": ccmni0 is present")
			ccmni0_ip = execute_Command("ip -o -4 addr list ccmni0 | awk '{print $4}' | cut -d/ -f1 | wc -w")
			if (int(ccmni0_ip) != 0):
				# print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": ccmni0 is connected")
				logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": ccmni0 is connected: ")
			else:
				logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": ccmni0 is NOT connected: " + ip_o_addr_list)

		wwan0_ip=0
		wwan0_connected = execute_Command("ifconfig -a | grep '^wwan0' | wc -c")
		if (int(wwan0_connected) == 0):
			logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": wwan0 is not present")
		else:
			# print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": wwan0 is present")
			wwan0_ip = execute_Command("ip -o -4 addr list wwan0 | awk '{print $4}' | cut -d/ -f1 | wc -w")
			if (int(wwan0_ip) != 0):
				# print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": wwan0 is connected")
				logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": wwan0 is connected")
			else:
				logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": wwan0 is NOT connected: " + ip_o_addr_list)

		wlan0_ip=0
		wlan0_connected = execute_Command("ifconfig -a | grep '^wlan0' | wc -c")
		if (int(wlan0_connected) == 0):
			logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": wlan0 is not present")
		else:
			# print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": wlan0 is present")
			wlan0_ip = execute_Command("ip -o -4 addr list wlan0 | awk '{print $4}' | cut -d/ -f1 | wc -w")
			if (int(wlan0_ip) != 0):
				# print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": wlan0 is connected")
				logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": wlan0 is connected")
			else:
				logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": wlan0 is NOT connected: " + ip_o_addr_list)

		# Perform retry only, if any IP address is not available
		if (int(wlan0_ip) == 1 or int(eth0_ip) == 1 or int(eth1_ip) == 1 or int(ccmni0_ip) == 1 or int(wwan0_ip) == 1):
			logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Received IP address: " + ip_o_addr_list)
			break

		retryCount = retryCount + 1

		# Give some delay before we repeat iteration
		time.sleep(constants.TIME_FIVE_SECONDS)

	if (int(wlan0_ip) == 0 and int(eth0_ip) == 0 and int(eth1_ip) == 0 and int(ccmni0_ip) == 0 and int(wwan0_ip) == 0):
		# An assumption that if original folder exists, test is running already
		# Needs better optimization
		if os.path.isdir(os.path.join(constants.LOG_DIRECTORY_FULL_PATH, constants.ORIGINAL_FOLDER_NAME)):
			logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": IP address not available: original directory exists")

			try:
				with open(constants.JSON_CONFIG_FILE_TEST_PARAMETERS) as fileObjectConfigFileTestParameters:
					dataTestParameters = json.load(fileObjectConfigFileTestParameters)

					# Iterating through the json dict
					for stringParameter in dataTestParameters:
	
						# Perform case-insensitive comparison
						if (stringParameter.casefold() == "stop_on_error_network_connection".casefold()):
							if (dataTestParameters[stringParameter].casefold() == "yes".casefold()):
								logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": before writing file for stop_on_error for: " + stringParameter)

								try:
									with open(constants.STOP_ON_ERROR_FILE,"w") as fileObjectStopOnError:
										fileObjectStopOnError.write (str("STOP_ON_ERROR"))

								except (OSError, IOError) as exception:
									logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

								logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": after writing files for stop_on_error")

							else:
								logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": stop_on_error for network connection is NOT enabled")

			except (OSError, IOError, KeyError, json.decoder.JSONDecodeError) as exception:
				logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))
				exit()

		# An assumption that if original folder does not exist, function is called for first time from start
		else:
			logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": IP address not available: original directory does not exist")

			print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": any network IP address is NOT available. Exiting script")
			logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": any network IP address is NOT available. Exiting script")

			# store end time
			logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Calling sync")
			execute_Command("sync")
			endTime = time.time()

			logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Time taken for function execution: " + str(int(endTime-startTime)))

			exit()
			
	else:
		print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": network is available")
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": network is available")

	# store end time
	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Calling sync")
	execute_Command("sync")
	endTime = time.time()

	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Time taken for function execution: " + str(int(endTime-startTime)))

def ensure_charger_connected():
	"""
	Purpose: Ensure that DUT is connected to charger when iterations are more than 50.
	If charger is not connected, it prompts user to connect to charger and exits the script.
	This stops any further test execution.

	Parameters: None

	Returns: None
    """

	""" Create frame object """
	frameObj = currentframe()

	""" String to track current function name """
	functionName = str(frameObj.f_code.co_name) + "()" # Function name

	# store starting time
	startTime = time.time()

	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Entered")

	charger_connected = int(execute_Command("power_supply_info 2>/dev/null | grep 'online:' | grep 'yes' | wc -l"))
	if (charger_connected == 1):
		print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": Charger connected")
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Charger connected")
	else:
		print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": Charger is NOT connected. Exiting script")
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Charger is NOT connected. Exiting script")

		# store end time
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Calling sync")
		execute_Command("sync")
		endTime = time.time()

		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Time taken for function execution: " + str(int(endTime-startTime)))

		exit()

	# store end time
	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Calling sync")
	execute_Command("sync")
	endTime = time.time()

	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Time taken for function execution: " + str(int(endTime-startTime)))
