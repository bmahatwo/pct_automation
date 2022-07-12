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
import zipfile
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

try:
	logging.basicConfig(filename=constants.LOG_FILE, level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')
except (FileNotFoundError,OSError, IOError) as exception:
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": exiting script")
	exit()

logger = logging.getLogger(__name__)

logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": SCRIPT_VERSION: " + constants.SCRIPT_VERSION)

""" Getting the length of command-line arguments """
numberOfArguments = len(sys.argv)

""" Allow only maximum 1 argument. First argument is file name """
if (numberOfArguments != 1):
	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": numberOfArguments != 1: " + str(numberOfArguments))

	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": exiting script")
	exit()
else:
	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": numberOfArguments:" + str(numberOfArguments))

if os.path.isdir(constants.LOG_DIRECTORY_FULL_PATH):
	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": directory exists: " + constants.LOG_DIRECTORY_FULL_PATH)
else:
	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": directory does not exist: " + constants.LOG_DIRECTORY_FULL_PATH)

	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": exiting script")
	exit()

if os.path.isfile(constants.CONF_FILE_ETC_INIT):
	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file exists: " + constants.CONF_FILE_ETC_INIT)
else:
	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file does not exist: " + constants.CONF_FILE_ETC_INIT)

	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": exiting script")
	exit()

if os.path.isfile(constants.COUNT_TARGET_FILE):
	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file exists:" + constants.COUNT_TARGET_FILE)
else:
	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file does not exist: " + constants.COUNT_TARGET_FILE)

	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": exiting script")
	exit()

originalFolderWithCompletePath = os.path.join(constants.LOG_DIRECTORY_FULL_PATH, constants.ORIGINAL_FOLDER_NAME)

iterationFolderCompletePath = ""

if os.path.isdir(originalFolderWithCompletePath):
	currentIteration = int (execute_save_compare.check_iterations_remaining())

	# Returns a datetime object containing the local date and time
	nowTimeDate = datetime.datetime.now()
	stringFolderName_NowTimeDate = str(currentIteration) + "_" + nowTimeDate.strftime("%d%m%Y_%H%M%S") + "_" + constants.STRING_COLD_BOOT_FROM_G3_DETAILED

	iterationFolderCompletePath = os.path.join(constants.LOG_DIRECTORY_FULL_PATH, stringFolderName_NowTimeDate)

	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": folder timestamp calling " + stringFolderName_NowTimeDate)

	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Received from check_iterations_remaining(): " + str(currentIteration))

	# Cold boot: prev_sleep_state 5
	# Warm boot: prev_sleep_state 0
	execute_save_compare.compare_prev_sleep_state(constants.PREV_SLEEP_STATE_COLD_BOOT, iterationFolderCompletePath)

	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": After calling compare_prev_sleep_state()")

	execute_save_compare.measure_time_between_each_iteration(constants.CONST_ITERATION_TIME_OF_COLD_BOOT_FROM_G3_DETAILED, iterationFolderCompletePath)

	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": After calling measure_time_between_each_iteration()")

	execute_save_compare.save_detailed_logs(iterationFolderCompletePath)

	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": After calling save_detailed_logs()")

	execute_save_compare.compare_logs(originalFolderWithCompletePath, iterationFolderCompletePath)

	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": After calling compare_logs()")

	execute_save_compare.copy_crash_log_files(iterationFolderCompletePath)

	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": After calling copy_crash_log_files()")

	execute_save_compare.check_errors_during_iteration(iterationFolderCompletePath, constants.ERROR_STRING_DMESG)

	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": After calling check_errors_during_iteration() with constants.ERROR_STRING_DMESG")

	execute_save_compare.check_errors_during_iteration(iterationFolderCompletePath, constants.ERROR_STRING_EC)

	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": After calling check_errors_during_iteration() with constants.ERROR_STRING_EC")

	execute_save_compare.check_errors_during_iteration(iterationFolderCompletePath, constants.ERROR_STRING_MMCLI)

	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": After calling check_errors_during_iteration() with constants.ERROR_STRING_MMCLI")

	execute_save_compare.check_errors_during_iteration(iterationFolderCompletePath, constants.ERROR_STRING_TYPECD)

	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": After calling check_errors_during_iteration() with constants.ERROR_STRING_TYPECD")

	# execute_save_compare.parse_bootstat_Summary(iterationFolderCompletePath)
	execute_save_compare.measure_bootperf(iterationFolderCompletePath)

	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Before ensure_network_connection()")

	execute_save_compare.ensure_network_connection(iterationFolderCompletePath)

	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Before calling move_var_log_messages_folder()")

	execute_save_compare.move_var_log_messages_folder(iterationFolderCompletePath)

	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": After calling check_stop_on_error_status()")

	execute_save_compare.check_stop_on_error_status()

	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": After calling check_stop_on_error_status()")

	execute_save_compare.check_retain_status_and_delete_files(iterationFolderCompletePath)

	logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": After calling check_retain_status_and_delete_files()")

else:
	logger.info (originalFolderWithCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": original folder does not exist. Creating: " + originalFolderWithCompletePath)

	# Cold boot: prev_sleep_state 5
	# Warm boot: prev_sleep_state 0
	execute_save_compare.compare_prev_sleep_state(constants.PREV_SLEEP_STATE_COLD_BOOT, originalFolderWithCompletePath)

	logger.info (originalFolderWithCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": After calling compare_prev_sleep_state()")

	execute_save_compare.save_detailed_logs(originalFolderWithCompletePath)
	logger.info (originalFolderWithCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": After save_detailed_logs with: " + originalFolderWithCompletePath)

	execute_save_compare.check_errors_during_iteration(originalFolderWithCompletePath, constants.ERROR_STRING_DMESG)

	logger.info (originalFolderWithCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": After calling check_errors_during_iteration() with constants.ERROR_STRING_DMESG")

	execute_save_compare.check_errors_during_iteration(originalFolderWithCompletePath, constants.ERROR_STRING_EC)

	logger.info (originalFolderWithCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": After calling check_errors_during_iteration() with constants.ERROR_STRING_EC")

	execute_save_compare.check_errors_during_iteration(originalFolderWithCompletePath, constants.ERROR_STRING_MMCLI)

	logger.info (originalFolderWithCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": After calling check_errors_during_iteration() with constants.ERROR_STRING_MMCLI")

	execute_save_compare.check_errors_during_iteration(originalFolderWithCompletePath, constants.ERROR_STRING_TYPECD)

	logger.info (originalFolderWithCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": After calling check_errors_during_iteration() with constants.ERROR_STRING_TYPECD")

	execute_save_compare.measure_filesize_for_original(originalFolderWithCompletePath)

	logger.info (originalFolderWithCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": After calling measure_filesize_for_original()")

	if os.path.exists (constants.VAR_LOG_MESSAGES_FULL_PATH):
		try:
			logger.info (originalFolderWithCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": file exists: " + constants.VAR_LOG_MESSAGES_FULL_PATH)
			os.remove (constants.VAR_LOG_MESSAGES_FULL_PATH)
			logger.info (originalFolderWithCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": after file removal: " + constants.VAR_LOG_MESSAGES_FULL_PATH)
		except (OSError, IOError) as exception:
			logger.info (originalFolderWithCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Before clearing /var/log/net.log")

execute_save_compare.clear_net_log(iterationFolderCompletePath)

logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Before deleting /var/log/typecd.log")

execute_save_compare.clear_typecd_log(iterationFolderCompletePath)

logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": before calling shutdown")

execute_save_compare.execute_Command("ectool reboot_ap_on_g3")
execute_save_compare.execute_Command("shutdown -h now")

logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": after calling shutdown")

execute_save_compare.start_shutdown_reboot_counter(stringFolderName_NowTimeDate, constants.TIME_TEN_SECONDS)
