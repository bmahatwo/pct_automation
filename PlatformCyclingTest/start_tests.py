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

""" Import suspend resume tests for usage """
import suspend_resume_tests_S0ix

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

""" Clean up older logs """
print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": Before cleanup_old_files()")
execute_save_compare.cleanup_old_files()
print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": After cleanup_old_files()")

# Check if all JSON files are with correct syntax
print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": Checking " + constants.JSON_CONFIG_FILE_COMPARE_LOGS)
try:
	with open(constants.JSON_CONFIG_FILE_COMPARE_LOGS) as fileObject:
		data = json.load(fileObject)

except (OSError, IOError, KeyError, json.decoder.JSONDecodeError) as exception:
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": exiting script")
	exit()

print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": Checking " + constants.JSON_CONFIG_FILE_ERROR_STRINGS)
try:
	with open(constants.JSON_CONFIG_FILE_ERROR_STRINGS) as fileObject:
		data = json.load(fileObject)
except (OSError, IOError, KeyError, json.decoder.JSONDecodeError) as exception:
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": exiting script")
	exit()

print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": Checking " + constants.JSON_CONFIG_FILE_COPY_DUT_FILES)
try:
	with open(constants.JSON_CONFIG_FILE_COPY_DUT_FILES) as fileObject:
		data = json.load(fileObject)
except (OSError, IOError, KeyError, json.decoder.JSONDecodeError) as exception:
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": exiting script")
	exit()

print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": Checking " + constants.JSON_CONFIG_FILE_SAVE_DETAILED_LOGS)
try:
	with open(constants.JSON_CONFIG_FILE_SAVE_DETAILED_LOGS) as fileObject:
		data = json.load(fileObject)
except (OSError, IOError, KeyError, json.decoder.JSONDecodeError) as exception:
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": exiting script")
	exit()

print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": Checking " + constants.JSON_CONFIG_FILE_SAVE_QUICK_LOGS)
try:
	with open(constants.JSON_CONFIG_FILE_SAVE_QUICK_LOGS) as fileObject:
		data = json.load(fileObject)
except (OSError, IOError, KeyError, json.decoder.JSONDecodeError) as exception:
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": exiting script")
	exit()

print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": Checking " + constants.JSON_CONFIG_FILE_TEST_PARAMETERS)
try:
	with open(constants.JSON_CONFIG_FILE_TEST_PARAMETERS) as fileObject:
		data = json.load(fileObject)

		# Iterating through JSON dict
		print ("\n**************")
		for stringParameter in data:
			print (stringParameter + " : " + str(data[stringParameter]))
		print ("**************\n")
		time.sleep (constants.TIME_TWO_SECONDS)

except (OSError, IOError, KeyError, json.decoder.JSONDecodeError) as exception:
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": exiting script")
	exit()

if os.path.isdir(constants.LOG_DIRECTORY_FULL_PATH):
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": directory exists: " + constants.LOG_DIRECTORY_FULL_PATH)
else:
	try:
		print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": directory does not exist: " + constants.LOG_DIRECTORY_FULL_PATH)
		os.mkdir(constants.LOG_DIRECTORY_FULL_PATH)
		print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": directory created: " + constants.LOG_DIRECTORY_FULL_PATH)
	except (FileNotFoundError, OSError, IOError) as exception:
		print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

		print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": exiting script")
		exit()
try:
	logging.basicConfig(filename=constants.LOG_FILE, level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')
except (FileNotFoundError, OSError, IOError) as exception:
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": exiting script")
	exit()

logger = logging.getLogger(__name__)

logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": SCRIPT_VERSION: " + constants.SCRIPT_VERSION)

""" Getting the length of command-line arguments """
numberOfArguments = len(sys.argv)

""" Allow only maximum 2 arguments First argument is file name """
if (numberOfArguments > 3):
	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": numberOfArguments > 3")
	execute_save_compare.show_Help()

	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": exiting script")
	exit()
else:
	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": numberOfArguments:" + str(numberOfArguments))

""" Read the argument as integer. First argument is test case number """
argumentTestCase = 0
if (numberOfArguments == 2 or numberOfArguments == 3):
	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": argumentTestCase ")
	argumentTestCase = int(sys.argv[1])

argumentNumberOfIterations = 0
if (numberOfArguments == 3):
	""" Read the argument as integer. Second argument is number of iterations """
	argumentNumberOfIterations = int(sys.argv[2])

	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": argumentNumberOfIterations: " + str(argumentNumberOfIterations))

""" Ensure argument to indicate test case is between desired range """
if (argumentTestCase < 1 or argumentTestCase > 13):
	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": argumentTestCase < 1 or argumentTestCase > 13")
	execute_save_compare.show_Help()

	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": exiting script")
	exit()

""" Ensure argument to indicate number of iterations case is between desired range for cycling tests """
if (argumentTestCase > 2 and (argumentNumberOfIterations < 1 or argumentNumberOfIterations > 10000)):
	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": argumentNumberOfIterations < 3 or argumentNumberOfIterations > 10000")
	execute_save_compare.show_Help()

	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": exiting script")
	exit()

if (argumentNumberOfIterations > 50):
	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": argumentNumberOfIterations > 50")
	execute_save_compare.ensure_charger_connected()

logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + " content of file " + constants.JSON_CONFIG_FILE_TEST_PARAMETERS + " :\n" + execute_save_compare.execute_Command("cat " + constants.JSON_CONFIG_FILE_TEST_PARAMETERS))

logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + " content of file " + constants.JSON_CONFIG_FILE_COMPARE_LOGS + " :\n" + execute_save_compare.execute_Command("cat " + constants.JSON_CONFIG_FILE_COMPARE_LOGS))

""" Switch-case works only in Python 3.10 and above """
if (argumentTestCase == 1):
	""" 1: Disable ssd root verification. Do not pass any parameters """
	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": case 1: Disable ssd root verification")

	execute_save_compare.execute_Command("/usr/share/vboot/bin/make_dev_ssd.sh --force --remove_rootfs_verification")

	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Before calling reboot")
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": Before calling reboot")
	execute_save_compare.execute_Command("reboot")

elif (argumentTestCase == 2):
	""" 2: Capture logs for saving original. Do not pass any parameters """
	originalFolderWithCompletePath = os.path.join(constants.LOG_DIRECTORY_FULL_PATH, constants.ORIGINAL_FOLDER_NAME)

	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": case 2: Capture logs for saving " + originalFolderWithCompletePath)

	if os.path.isdir(originalFolderWithCompletePath):
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": original directory exists")
		try:
			shutil.rmtree(originalFolderWithCompletePath)
			logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": after remove dir")
		except (OSError, IOError) as exception:
			logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))

	try:
		os.mkdir(originalFolderWithCompletePath)
	except (FileNotFoundError,OSError, IOError) as exception:
		logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": error: " + str(exception))
		exit()

	execute_save_compare.ensure_network_connection()

	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": Before calling save_detailed_logs()")
	execute_save_compare.save_detailed_logs(originalFolderWithCompletePath)
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": After calling save_detailed_logs()")

	execute_save_compare.kill_specific_process("dmesg")
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": Completed saving original logs")

elif (argumentTestCase == 3):
	""" 3: Run Cold Boot Test from S5. Pass parameter for number of iterations. (pre-requisite : Disable ssd root verification and then perform this step) """
	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": case 3: Run Cold Boot Test from S5")

	execute_save_compare.ensure_network_connection()
	execute_save_compare.ensure_rootfs_verification_disabled()
	execute_save_compare.clear_older_crash_log_files()
	execute_save_compare.clear_elogtool_log()
	execute_save_compare.clear_net_log()
	execute_save_compare.clear_typecd_log()

	""" Copy autotest files to location """
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": Before calling copy_autotest_files()")
	execute_save_compare.copy_autotest_files()

	""" Copy target count to file """
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": Before calling write_target_count()")
	execute_save_compare.write_target_count(argumentNumberOfIterations)

	""" Write conf file to location """
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": Before calling write_CONF_FILE_ETC_INIT()")
	execute_save_compare.write_CONF_FILE_ETC_INIT(constants.CONF_FILE_ETC_INIT_COLD_BOOT_S5_DETAILED_TESTS)

	""" Write test operation to file """
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": Before writing test operation file")
	execute_save_compare.write_string_to_file(constants.STRING_COLD_BOOT_FROM_S5_DETAILED, constants.STRING_TEST_OPERATION_FILE)

	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Before calling shutdown")
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": Before calling shutdown")

	execute_save_compare.execute_Command("ectool reboot_ec cold at-shutdown")
	execute_save_compare.execute_Command("shutdown -h now")
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": After calling shutdown")

elif (argumentTestCase == 4):
	""" 4: Run Cold Boot Test from G3. Pass parameter for number of iterations. """
	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": case 4: Run Cold Boot Test from G3")

	execute_save_compare.ensure_network_connection()
	execute_save_compare.ensure_rootfs_verification_disabled()
	execute_save_compare.clear_older_crash_log_files()
	execute_save_compare.clear_elogtool_log()
	execute_save_compare.clear_net_log()
	execute_save_compare.clear_typecd_log()

	""" Copy autotest files to location """
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": Before calling copy_autotest_files()")
	execute_save_compare.copy_autotest_files()

	""" Copy target count to file """
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": Before calling write_target_count()")
	execute_save_compare.write_target_count(argumentNumberOfIterations)

	""" Write conf file to location """
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": Before calling write_CONF_FILE_ETC_INIT()")
	execute_save_compare.write_CONF_FILE_ETC_INIT(constants.CONF_FILE_ETC_INIT_COLD_BOOT_G3_DETAILED_TESTS)

	""" Write test operation to file """
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": Before writing test operation file")
	execute_save_compare.write_string_to_file(constants.STRING_COLD_BOOT_FROM_G3_DETAILED, constants.STRING_TEST_OPERATION_FILE)

	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Before calling shutdown")
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": Before calling shutdown")

	execute_save_compare.execute_Command("ectool reboot_ap_on_g3")
	execute_save_compare.execute_Command("shutdown -h now")
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": After calling shutdown")

elif (argumentTestCase == 5):
	""" 5: Run Cold Boot Quick Test (S0-S5). Pass parameter for number of iterations. """
	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": case 5: Run Cold Boot Quick Test (S0-S5)")

	execute_save_compare.ensure_network_connection()
	execute_save_compare.ensure_rootfs_verification_disabled()
	execute_save_compare.clear_older_crash_log_files()
	execute_save_compare.clear_elogtool_log()
	execute_save_compare.clear_net_log()
	execute_save_compare.clear_typecd_log()

	""" Copy target count to file """
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": Before calling write_target_count()")
	execute_save_compare.write_target_count(argumentNumberOfIterations)

	""" Write conf file to location """
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": Before calling write_CONF_FILE_ETC_INIT()")
	execute_save_compare.write_CONF_FILE_ETC_INIT(constants.CONF_FILE_ETC_INIT_COLD_BOOT_S5_QUICK_TESTS)

	""" Write test operation to file """
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": Before writing test operation file")
	execute_save_compare.write_string_to_file(constants.STRING_COLD_BOOT_FROM_S5_QUICK, constants.STRING_TEST_OPERATION_FILE)

	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Before calling shutdown")
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": Before calling shutdown")

	execute_save_compare.execute_Command("ectool reboot_ec cold at-shutdown")
	execute_save_compare.execute_Command("shutdown -h now")
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": After calling shutdown")

elif (argumentTestCase == 6):
	""" 6: Run Cold Boot Quick Test (S0-S5-G3). Pass parameter for number of iterations. """
	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": case 6: Run Cold Boot Quick Test (S0-S5-G3)")

	execute_save_compare.ensure_network_connection()
	execute_save_compare.ensure_rootfs_verification_disabled()
	execute_save_compare.clear_older_crash_log_files()
	execute_save_compare.clear_elogtool_log()
	execute_save_compare.clear_net_log()
	execute_save_compare.clear_typecd_log()

	""" Copy target count to file """
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": Before calling write_target_count()")
	execute_save_compare.write_target_count(argumentNumberOfIterations)

	""" Write conf file to location """
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": Before calling write_CONF_FILE_ETC_INIT()")
	execute_save_compare.write_CONF_FILE_ETC_INIT(constants.CONF_FILE_ETC_INIT_COLD_BOOT_G3_QUICK_TESTS)

	""" Write test operation to file """
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": Before writing test operation file")
	execute_save_compare.write_string_to_file(constants.STRING_COLD_BOOT_FROM_G3_QUICK, constants.STRING_TEST_OPERATION_FILE)

	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Before calling shutdown")
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": Before calling shutdown")

	execute_save_compare.execute_Command("ectool reboot_ap_on_g3")
	execute_save_compare.execute_Command("shutdown -h now")
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": After calling shutdown")

elif (argumentTestCase == 7):
	""" 7: Run Warm Boot Test. Pass parameter for number of iterations. (pre-requisite : Disable ssd root verification and then perform this step) """
	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": case 7: Run Warm Boot Test")

	execute_save_compare.ensure_network_connection()
	execute_save_compare.ensure_rootfs_verification_disabled()
	execute_save_compare.clear_older_crash_log_files()
	execute_save_compare.clear_elogtool_log()
	execute_save_compare.clear_net_log()
	execute_save_compare.clear_typecd_log()

	""" Copy autotest files to location """
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": Before calling copy_autotest_files()")
	execute_save_compare.copy_autotest_files()

	""" Copy target count to file """
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": Before calling write_target_count()")
	execute_save_compare.write_target_count(argumentNumberOfIterations)

	""" Write conf file to location """
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": Before calling write_CONF_FILE_ETC_INIT()")
	execute_save_compare.write_CONF_FILE_ETC_INIT(constants.CONF_FILE_ETC_INIT_WARM_BOOT_DETAILED_TESTS)

	""" Write test operation to file """
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": Before writing test operation file")
	execute_save_compare.write_string_to_file(constants.STRING_WARM_BOOT_DETAILED, constants.STRING_TEST_OPERATION_FILE)

	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Before calling reboot")
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": Before calling reboot")

	execute_save_compare.execute_Command("reboot")
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": After calling reboot")

elif (argumentTestCase == 8):
	""" 8: Run Warm Boot Quick Test. Pass parameter for number of iterations. """
	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": case 8: Run Warm Boot Quick Test")

	execute_save_compare.ensure_network_connection()
	execute_save_compare.ensure_rootfs_verification_disabled()
	execute_save_compare.clear_older_crash_log_files()
	execute_save_compare.clear_elogtool_log()
	execute_save_compare.clear_net_log()
	execute_save_compare.clear_typecd_log()

	""" Copy target count to file """
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": Before calling write_target_count()")
	execute_save_compare.write_target_count(argumentNumberOfIterations)

	""" Write conf file to location """
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": Before calling write_CONF_FILE_ETC_INIT()")
	execute_save_compare.write_CONF_FILE_ETC_INIT(constants.CONF_FILE_ETC_INIT_WARM_BOOT_QUICK_TESTS)

	""" Write test operation to file """
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": Before writing test operation file")
	execute_save_compare.write_string_to_file(constants.STRING_WARM_BOOT_QUICK, constants.STRING_TEST_OPERATION_FILE)

	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Before calling reboot")
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": Before calling reboot")

	execute_save_compare.execute_Command("reboot")
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": After calling reboot")

elif (argumentTestCase == 9):
	""" 9: Run Suspend-Resume Stress test for S0ix. Pass parameter for number of iterations. """
	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": case 9: Run Suspend-Resume Stress test for S0ix")

	execute_save_compare.ensure_network_connection()
	execute_save_compare.clear_older_crash_log_files()
	execute_save_compare.clear_net_log()

	""" Copy target count to file """
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": Before calling write_target_count()")
	execute_save_compare.write_target_count(argumentNumberOfIterations)

	""" Write test operation to file """
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": Before writing test operation file")
	execute_save_compare.write_string_to_file(constants.STRING_SUSPEND_RESUME_S0ix, constants.STRING_TEST_OPERATION_FILE)

	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": Before calling execute_suspend_resume()")
	suspend_resume_tests_S0ix.execute_suspend_resume(argumentNumberOfIterations)

	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Tests are finished completely")
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": Tests are finished completely")

elif (argumentTestCase == 10):
	""" 10. Run Cold Boot Quick Test (S0-S5) + suspend-resume quick test. Pass parameter for number of iterations for cold boot (S0-S5). Suspend resume iterations are hard-coded. """
	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": case 10: Run Cold Boot Quick Test (S0-S5) + suspend-resume quick test")

	execute_save_compare.ensure_network_connection()
	execute_save_compare.ensure_rootfs_verification_disabled()
	execute_save_compare.clear_older_crash_log_files()
	execute_save_compare.clear_elogtool_log()
	execute_save_compare.clear_net_log()
	execute_save_compare.clear_typecd_log()

	""" Copy target count to file """
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": Before calling write_target_count()")
	execute_save_compare.write_target_count(argumentNumberOfIterations)

	""" Write conf file to location """
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": Before calling write_CONF_FILE_ETC_INIT()")
	execute_save_compare.write_CONF_FILE_ETC_INIT(constants.CONF_FILE_ETC_INIT_COLD_BOOT_S5_SUSPEND_RESUME_QUICK_TESTS)

	""" Write test operation to file """
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": Before writing test operation file")
	execute_save_compare.write_string_to_file(constants.STRING_COLD_BOOT_FROM_S5_SUSPEND_RESUME_QUICK, constants.STRING_TEST_OPERATION_FILE)

	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Before calling shutdown")
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": Before calling shutdown")

	execute_save_compare.execute_Command("ectool reboot_ec cold at-shutdown")
	execute_save_compare.execute_Command("shutdown -h now")
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": After calling shutdown")

elif (argumentTestCase == 11):
	""" 11. Run Cold Boot Quick Test (S0-S5-G3) + suspend-resume quick test. Pass parameter for number of iterations for cold boot (S0-S5-G3). Suspend resume iterations are hard-coded. """
	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": case 11: Run Cold Boot Quick Test (S0-S5-G3) + suspend-resume quick test")

	execute_save_compare.ensure_network_connection()
	execute_save_compare.ensure_rootfs_verification_disabled()
	execute_save_compare.clear_older_crash_log_files()
	execute_save_compare.clear_elogtool_log()
	execute_save_compare.clear_net_log()
	execute_save_compare.clear_typecd_log()

	""" Copy target count to file """
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": Before calling write_target_count()")
	execute_save_compare.write_target_count(argumentNumberOfIterations)

	""" Write conf file to location """
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": Before calling write_CONF_FILE_ETC_INIT()")
	execute_save_compare.write_CONF_FILE_ETC_INIT(constants.CONF_FILE_ETC_INIT_COLD_BOOT_G3_SUSPEND_RESUME_QUICK_TESTS)

	""" Write test operation to file """
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": Before writing test operation file")
	execute_save_compare.write_string_to_file(constants.STRING_COLD_BOOT_FROM_G3_SUSPEND_RESUME_QUICK, constants.STRING_TEST_OPERATION_FILE)

	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Before calling shutdown")
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": Before calling shutdown")

	execute_save_compare.execute_Command("ectool reboot_ec cold at-shutdown")
	execute_save_compare.execute_Command("shutdown -h now")
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": After calling shutdown")

elif (argumentTestCase == 12):
	""" 12. Run Warm Boot Quick Test + suspend-resume quick test. Pass parameter for number of iterations for warm boot. Suspend resume iterations are hard-coded. """
	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": case 12: Run Warm Boot Quick Test + suspend-resume quick test")

	execute_save_compare.ensure_network_connection()
	execute_save_compare.ensure_rootfs_verification_disabled()
	execute_save_compare.clear_older_crash_log_files()
	execute_save_compare.clear_elogtool_log()
	execute_save_compare.clear_net_log()
	execute_save_compare.clear_typecd_log()

	""" Copy target count to file """
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": Before calling write_target_count()")
	execute_save_compare.write_target_count(argumentNumberOfIterations)

	""" Write conf file to location """
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": Before calling write_CONF_FILE_ETC_INIT()")
	execute_save_compare.write_CONF_FILE_ETC_INIT(constants.CONF_FILE_ETC_INIT_WARM_BOOT_SUSPEND_RESUME_QUICK_TESTS)

	""" Write test operation to file """
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": Before writing test operation file")
	execute_save_compare.write_string_to_file(constants.STRING_WARM_BOOT_SUSPEND_RESUME_QUICK, constants.STRING_TEST_OPERATION_FILE)

	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Before calling shutdown")
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": Before calling shutdown")

	execute_save_compare.execute_Command("ectool reboot_ec cold at-shutdown")
	execute_save_compare.execute_Command("shutdown -h now")
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": After calling shutdown")

elif (argumentTestCase == 13):
	""" 13. Run Cold Boot Quick Test (S0-S5-G3) + warm boot quick test. Pass parameter for total number of iterations (warm + cold). """
	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": case 13: Run Cold Boot Quick Test (S0-S5-G3) + warm boot quick test. Pass parameter for total number of iterations (warm + cold).")

	execute_save_compare.ensure_network_connection()
	execute_save_compare.ensure_rootfs_verification_disabled()
	execute_save_compare.clear_older_crash_log_files()
	execute_save_compare.clear_elogtool_log()
	execute_save_compare.clear_net_log()
	execute_save_compare.clear_typecd_log()

	""" Copy target count to file """
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": Before calling write_target_count()")
	execute_save_compare.write_target_count(argumentNumberOfIterations)

	""" Write conf file to location """
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": Before calling write_CONF_FILE_ETC_INIT()")
	execute_save_compare.write_CONF_FILE_ETC_INIT(constants.CONF_FILE_ETC_INIT_COLD_BOOT_G3_WARM_BOOT_QUICK_TESTS)

	""" Write test operation to file """
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": Before writing test operation file")
	execute_save_compare.write_string_to_file(constants.STRING_COLD_BOOT_FROM_G3_WARM_BOOT_QUICK, constants.STRING_TEST_OPERATION_FILE)

	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Before calling shutdown")
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": Before calling shutdown")

	execute_save_compare.execute_Command("ectool reboot_ec cold at-shutdown")
	execute_save_compare.execute_Command("shutdown -h now")
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": After calling shutdown")

else:
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": Something else")
	logger.info (fileName + ": " + functionName + ": line " + str(frameObj.f_lineno) + ": Something else")
	pass
