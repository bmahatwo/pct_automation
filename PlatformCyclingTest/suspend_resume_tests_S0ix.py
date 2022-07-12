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

logger = logging.getLogger(__name__)

logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": SCRIPT_VERSION: " + constants.SCRIPT_VERSION)

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

def execute_suspend_resume(argumentNumberOfIterations):
	"""
	Purpose: execute suspend-resume tests

	Parameters:
	command: int: indicates number of iterations to execute suspend-resume

	Returns: None

    """

	""" Create frame object """
	frameObj = currentframe()

	""" String to track current function name """
	functionName = str(frameObj.f_code.co_name) + "()" # Function name

	if os.path.isfile(constants.LOG_FILE):
		print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": log file exists: " + constants.LOG_FILE)
	else:
		print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": log file does not exist: " + constants.LOG_FILE)

	if os.path.isdir(constants.LOG_DIRECTORY_FULL_PATH):
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": directory exists: " + constants.LOG_DIRECTORY_FULL_PATH)
	else:
		print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": directory does not exist: " + constants.LOG_DIRECTORY_FULL_PATH)

		print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": exiting script")
		exit()

	originalFolderWithCompletePath = os.path.join(constants.LOG_DIRECTORY_FULL_PATH, constants.ORIGINAL_FOLDER_NAME)

	""" Store original logs before tests start """
	if os.path.isdir(originalFolderWithCompletePath):
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": original folder exists " + originalFolderWithCompletePath)
		print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": original folder exists")

		print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": exiting script")
		exit()

	else:
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": original folder does not exist. Creating: " + originalFolderWithCompletePath)
		print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": saving logs for original folder")

		# Clear off dmesg logs before we dump original logs
		execute_save_compare.execute_Command("dmesg -c")

		execute_save_compare.save_detailed_logs(originalFolderWithCompletePath)
		print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": saved logs for original folder")

		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": After save_detailed_logs with: " + constants.ORIGINAL_FOLDER_NAME)

		# Copy original iteration's file in parent folder of log location
		if os.path.isfile(os.path.join(originalFolderWithCompletePath, "substate_residencies_original.txt")):
			logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": substate_residencies_original.txt present in original")
			shutil.copy(os.path.join(originalFolderWithCompletePath, "substate_residencies_original.txt"), os.path.join(constants.LOG_DIRECTORY_FULL_PATH, "substate_residencies_original.txt"))
			logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": After copying substate_residencies_original.txt")

		execute_save_compare.measure_filesize_for_original(originalFolderWithCompletePath)

		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": After calling measure_filesize_for_original()")

	for currentIteration in range (argumentNumberOfIterations):

		# Returns a datetime object containing the local date and time
		nowTimeDate = datetime.datetime.now()
		stringFolderName_NowTimeDate = str(currentIteration + 1) + "_" + nowTimeDate.strftime("%d%m%Y_%H%M%S") + "_" + constants.STRING_SUSPEND_RESUME_S0ix

		iterationFolderCompletePath=os.path.join(constants.LOG_DIRECTORY_FULL_PATH, stringFolderName_NowTimeDate)

		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": folder timestamp calling " + stringFolderName_NowTimeDate)

		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": folder timestamp calling " + stringFolderName_NowTimeDate)

		execute_save_compare.measure_time_between_each_iteration(constants.CONST_ITERATION_TIME_OF_SUSPEND_RESUME_S0ix, iterationFolderCompletePath)

		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": After calling measure_time_between_each_iteration()")

		# Clear off dmesg logs before we perform test
		execute_save_compare.execute_Command("dmesg -c")

		print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": Before suspending: currentIteration: " + str(currentIteration + 1))
		time.sleep(constants.TIME_ONE_SECOND)
		string_suspend_stress_test_log=execute_save_compare.execute_Command("suspend_stress_test -c 1")

		print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": After suspending: currentIteration: " + str(currentIteration + 1))
		time.sleep(constants.TIME_FIVE_SECONDS)

		# Resume playback using SPACE key event from https://chromium.googlesource.com/chromiumos/third_party/autotest/+/main/client/cros/input_playback/keyboard_space
		# evemu-play –insert-slot0  $INPUT_DEVICE < $PATH_TO_KEY_EVENT_FILE

		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Before calling save_detailed_logs() with: " + iterationFolderCompletePath)

		print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": saving logs for: " + stringFolderName_NowTimeDate)
		
		execute_save_compare.save_detailed_logs(iterationFolderCompletePath)

		print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": saved logs for: " + stringFolderName_NowTimeDate)

		execute_save_compare.write_string_to_file(string_suspend_stress_test_log, os.path.join(iterationFolderCompletePath, "suspend_stress_test_log.txt"))
		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Before calling compare_logs() with: " + iterationFolderCompletePath)

		execute_save_compare.compare_logs(originalFolderWithCompletePath, iterationFolderCompletePath)

		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": After calling compare_logs()")

		execute_save_compare.copy_crash_log_files(iterationFolderCompletePath)

		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": After calling copy_crash_log_files()")

		execute_save_compare.perform_checks_for_suspend_resume(iterationFolderCompletePath)

		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": After calling perform_checks_for_suspend_resume()")

		execute_save_compare.check_errors_during_iteration(iterationFolderCompletePath, constants.ERROR_STRING_DMESG)

		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": After calling check_errors_during_iteration() with constants.ERROR_STRING_DMESG")

		execute_save_compare.check_errors_during_iteration(iterationFolderCompletePath, constants.ERROR_STRING_MMCLI)

		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": After calling check_errors_during_iteration() with constants.ERROR_STRING_MMCLI")

		execute_save_compare.ensure_network_connection(iterationFolderCompletePath)

		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": After calling ensure_network_connection()")

		execute_save_compare.check_stop_on_error_status()

		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": After calling check_stop_on_error_status()")

		execute_save_compare.check_retain_status_and_delete_files(iterationFolderCompletePath)

		logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": After calling check_retain_status_and_delete_files()")

		execute_save_compare.clear_net_log(iterationFolderCompletePath)

		""" Syntax to read: CURRENT_COUNT=3 """
		try:
				stringCountCompleted = "CURRENT_COUNT=" + str(currentIteration + 1)

				logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": currentIteration: " + str(currentIteration + 1))

				execute_save_compare.write_string_to_file(stringCountCompleted, constants.COUNT_COMPLETED_FILE)
				logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": write completed: " + constants.COUNT_COMPLETED_FILE)

		except (OSError, IOError) as exception:
			logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

			logger.info (iterationFolderCompletePath + ": " + fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": exiting script")
			exit()

	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": After finishing all iterations of suspend-resume")
	execute_save_compare.save_error_summary()

	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": After calling save_error_summary()")
