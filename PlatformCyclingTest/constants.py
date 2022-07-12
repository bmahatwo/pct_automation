#!/usr/bin/python

import datetime
import difflib
import logging
import json
import os
import requests
import shutil
import sys
import subprocess
import time
from subprocess import Popen, PIPE
from inspect import currentframe, getframeinfo

SCRIPT_VERSION="28 June, 2022"

# Constants for sleep duration
TIME_ONE_SECOND=1
TIME_TWO_SECONDS=2
TIME_FIVE_SECONDS=5
TIME_EIGHT_SECONDS=8
TIME_TEN_SECONDS=10
TIME_FIFTEEN_SECONDS=15
TIME_TWENTY_SECONDS=20
TIME_FORTY_SECONDS=40
TIME_SIXTY_SECONDS=60
PCH_IP_POWER_GATING_STATUS_WAIT_COUNT=3
TARGET_COUNT=3 # Default value of iterations
NEXT_BOOT_COUNT=1
SUSPEND_RESUME_QUICK_TARGET_COUNT=3 # Default value of iterations

# Constants for test scenario
CONST_DISABLE_SSD_ROOTFS_VERIFICATION=1
CONST_CAPTURE_SAVE_ORIGINAL=2
CONST_COLD_BOOT_FROM_S5_DETAILED=3
CONST_COLD_BOOT_FROM_G3_DETAILED=4
CONST_COLD_BOOT_FROM_S5_QUICK=5
CONST_COLD_BOOT_FROM_G3_QUICK=6
CONST_WARM_BOOT_DETAILED=7
CONST_WARM_BOOT_QUICK=8
CONST_SUSPEND_RESUME_S0ix=9

# Constants for folder name string
STRING_COLD_BOOT_FROM_S5_DETAILED="cold_boot_s0_s5_detailed"
STRING_COLD_BOOT_FROM_G3_DETAILED="cold_boot_s0_s5_g3_detailed"
STRING_COLD_BOOT_FROM_S5_QUICK="cold_boot_s0_s5_quick"
STRING_COLD_BOOT_FROM_G3_QUICK="cold_boot_s0_s5_g3_quick"
STRING_WARM_BOOT_DETAILED="warm_boot_detailed"
STRING_WARM_BOOT_QUICK="warm_boot_quick"
STRING_SUSPEND_RESUME_S0ix="suspend_resume_s0ix"
STRING_COLD_BOOT_FROM_S5_SUSPEND_RESUME_QUICK="cold_boot_s0_s5_suspend_resume_quick"
STRING_COLD_BOOT_FROM_G3_SUSPEND_RESUME_QUICK="cold_boot_s0_s5_g3_suspend_resume_quick"
STRING_WARM_BOOT_SUSPEND_RESUME_QUICK="warm_boot_suspend_resume_quick"
STRING_COLD_BOOT_FROM_G3_WARM_BOOT_QUICK="cold_boot_s0_s5_g3_warm_boot_quick"

# Constants for error strings comparison
ERROR_STRING_CONSOLERAMOOPS="console-ramoops"
ERROR_STRING_DMESG="dmesg"
ERROR_STRING_EC="ec"
ERROR_STRING_MMCLI="mmcli"
ERROR_STRING_TYPECD="typecd"

# Constants to identify time between each iteration of test
CONST_ITERATION_TIME_OF_COLD_BOOT_FROM_S5_DETAILED=60
CONST_ITERATION_TIME_OF_COLD_BOOT_FROM_G3_DETAILED=70
CONST_ITERATION_TIME_OF_COLD_BOOT_S5_QUICK=30
CONST_ITERATION_TIME_OF_COLD_BOOT_G3_QUICK=40
CONST_ITERATION_TIME_OF_WARM_BOOT_DETAILED=60
CONST_ITERATION_TIME_OF_WARM_BOOT_QUICK=30
CONST_ITERATION_TIME_OF_SUSPEND_RESUME_S0ix=50

CORP_PROXY = "http://proxy-iind.intel.com:911"

# Cold boot: prev_sleep_state 5
PREV_SLEEP_STATE_COLD_BOOT="prev_sleep_state 5"

# Warm boot: prev_sleep_state 0
PREV_SLEEP_STATE_WARM_BOOT="prev_sleep_state 0"

CONF_FILE_ETC_INIT="/etc/init/pct.conf"
SCRIPT_DIRECTORY="/usr/local/PlatformCyclingTest"
LOG_DIRECTORY_NAME="pct_logs"
LOG_DIRECTORY_FULL_PATH="/usr/local/pct_logs"

LOG_FILE = LOG_DIRECTORY_FULL_PATH + "/" + "cycling_time_log.log"
ERROR_DETAILS_FILE=LOG_DIRECTORY_FULL_PATH + "/" + "error_details.log"
ERROR_SUMMARY_FILE=LOG_DIRECTORY_FULL_PATH + "/" + "error_summary.log"
ERROR_ITERATIONS_FILE=LOG_DIRECTORY_FULL_PATH + "/" + "error_iterations.log"
PREVIOUS_TIMESTAMP_FILE = LOG_DIRECTORY_FULL_PATH + "/" + "previous_timestamp.log"
STRING_TEST_OPERATION_FILE = LOG_DIRECTORY_FULL_PATH + "/" + "test_operation.log"
STOP_ON_ERROR_FILE=LOG_DIRECTORY_FULL_PATH + "/" + "stop_on_error.log"
RETAIN_LOG_FILES=LOG_DIRECTORY_FULL_PATH + "/" + "retain_log_files.log"

LOGIN_HOME_DIRECTORY="/home/chronos/user/Downloads"

VAR_LOG_MESSAGES_FULL_PATH="/var/log/messages"
VAR_LOG_MESSAGES_FILE_NAME="messages"

JSON_CONFIG_FILE_COMPARE_LOGS = SCRIPT_DIRECTORY + "/" + "config_compare_logs.json"
JSON_CONFIG_FILE_COPY_DUT_FILES = SCRIPT_DIRECTORY + "/" + "config_copy_dut_files.json"
JSON_CONFIG_FILE_ERROR_STRINGS = SCRIPT_DIRECTORY + "/" + "config_error_strings.json"
JSON_CONFIG_FILE_SAVE_DETAILED_LOGS = SCRIPT_DIRECTORY + "/" + "config_save_detailed_logs.json"
JSON_CONFIG_FILE_SAVE_QUICK_LOGS = SCRIPT_DIRECTORY + "/" + "config_save_quick_logs.json"
JSON_CONFIG_FILE_TEST_PARAMETERS = SCRIPT_DIRECTORY + "/" + "config_test_parameters.json"

COUNT_COMPLETED_FILE = LOG_DIRECTORY_FULL_PATH + "/" + "count_completed.txt"
COUNT_TARGET_FILE = LOG_DIRECTORY_FULL_PATH + "/" + "count_target.txt"

ORIGINAL_FOLDER_NAME="original"

DESKTOPUI_SIMPLELOGIN_DIRECTORY_SCRIPT_PATH=SCRIPT_DIRECTORY + '/autotest_files/desktopui_SimpleLogin'

DESKTOPUI_SIMPLELOGIN_DIRECTORY_USR_LOCAL_PATH = '/usr/local/autotest/tests/desktopui_SimpleLogin'
DESKTOPUI_SIMPLELOGIN_PY_FILE_SCRIPT_PATH='/usr/local/autotest/tests/desktopui_SimpleLogin/desktopui_SimpleLogin.py'
DESKTOPUI_SIMPLELOGIN_CONTROL_FILE_USR_LOCAL_PATH='/usr/local/autotest/tests/desktopui_SimpleLogin/control'
DESKTOPUI_SIMPLELOGIN_PY_FILE_USR_LOCAL_PATH='/usr/local/autotest/tests/desktopui_SimpleLogin/desktopui_SimpleLogin.py'

# String constants
CBMEM_1_PREV_SLEEP_STATE="cbmem -1 | grep prev_sleep_state"

# Boot time file constants
FIRMWARE_BOOT_TIME="/tmp/firmware-boot-time"
UPTIME_LOGIN_PROMPT_VISIBLE="/tmp/uptime-login-prompt-visible"
TARGET_SECONDS_POWER_ON_TO_LOGIN_NORMAL_MODE=8.5
TARGET_SECONDS_POWER_ON_TO_LOGIN_DEVELOPER_MODE=12.5

# Constants used during execution
SUSPEND_TIME_TARGET_MSECS=1000
RESUME_TIME_TARGET_MSECS=1000

TEN_MINUTES_IN_SECONDS=600
COMMAND_TIMELIMIT=240
SCREENSHOT_MINIMUM_SIZE=36000
NUMBER_OF_LOG_FILES_PER_ITERATION=20
NUMBER_OF_DUMP_FILES_TOLERANCE_VALUE=50
HUNDRED_MB=104857600
TWO_HUNDRED_MB=209715200
ONE_MB=1048576
WGET_DOWNLOAD_RETRY_ATTEMPTS=3
IP_ADDRESS_RETRY_ATTEMPTS=3
WGET_DOWNLOAD_FILESIZE=3092061
WGET_HTTP_URL="http://storage.googleapis.com/chromiumos-test-assets-public/audio_test/audio.mp3"

TBT_ALPINE_RIDGE_DEVICE_ID="15d3"
TBT_TITAN_RIDGE_DEVICE_ID="15ef"

TOTAL_FILE_CONTENT_COMPARISON_DONE=0

CONF_FILE_ETC_INIT_COLD_BOOT_G3_QUICK_TESTS =  '''
# Date		:	''' + SCRIPT_VERSION + '''
description     "PlatformCyclingTest"
author          "Gulavani, Pallavi (pallavi.gulavani@intel.com), Narayan, Nupur (nupur.narayan@intel.com), Panse, Vrukesh V (vrukesh.v.panse@intel.com)"

start on starting system-services

script
  if [ -e /usr/local/PlatformCyclingTest/cold_boot_g3_quick_tests.py ]; then
    exec /usr/local/bin/python /usr/local/PlatformCyclingTest/cold_boot_g3_quick_tests.py
  fi
end script
'''

CONF_FILE_ETC_INIT_COLD_BOOT_G3_DETAILED_TESTS = '''
# Date		:	''' + SCRIPT_VERSION + '''
description     "PlatformCyclingTest"
author          "Gulavani, Pallavi (pallavi.gulavani@intel.com), Narayan, Nupur (nupur.narayan@intel.com), Panse, Vrukesh V (vrukesh.v.panse@intel.com)"

start on starting system-services

script
  if [ -e /usr/local/PlatformCyclingTest/cold_boot_detailed_tests_from_G3.py ]; then
    exec /usr/local/bin/python /usr/local/PlatformCyclingTest/cold_boot_detailed_tests_from_G3.py
  fi
end script
'''

CONF_FILE_ETC_INIT_COLD_BOOT_S5_DETAILED_TESTS = '''
# Date		:	''' + SCRIPT_VERSION + '''
description     "PlatformCyclingTest"
author          "Gulavani, Pallavi (pallavi.gulavani@intel.com), Narayan, Nupur (nupur.narayan@intel.com), Panse, Vrukesh V (vrukesh.v.panse@intel.com)"

start on starting system-services

script
  if [ -e /usr/local/PlatformCyclingTest/cold_boot_detailed_tests_from_S5.py ]; then
    exec /usr/local/bin/python /usr/local/PlatformCyclingTest/cold_boot_detailed_tests_from_S5.py
  fi
end script

'''

CONF_FILE_ETC_INIT_COLD_BOOT_S5_QUICK_TESTS = '''
# Date		:	''' + SCRIPT_VERSION + '''
description     "PlatformCyclingTest"
author          "Gulavani, Pallavi (pallavi.gulavani@intel.com), Narayan, Nupur (nupur.narayan@intel.com), Panse, Vrukesh V (vrukesh.v.panse@intel.com)"

start on starting system-services

script
  if [ -e /usr/local/PlatformCyclingTest/cold_boot_s5_quick_tests.py ]; then
    exec /usr/local/bin/python /usr/local/PlatformCyclingTest/cold_boot_s5_quick_tests.py
  fi
end script

'''

CONF_FILE_ETC_INIT_WARM_BOOT_QUICK_TESTS = '''
# Date		:	''' + SCRIPT_VERSION + '''
description     "PlatformCyclingTest"
author          "Gulavani, Pallavi (pallavi.gulavani@intel.com), Narayan, Nupur (nupur.narayan@intel.com), Panse, Vrukesh V (vrukesh.v.panse@intel.com)"

start on starting system-services

script
  if [ -e /usr/local/PlatformCyclingTest/warm_boot_quick_tests.py ]; then
    exec /usr/local/bin/python /usr/local/PlatformCyclingTest/warm_boot_quick_tests.py
  fi
end script
'''

CONF_FILE_ETC_INIT_WARM_BOOT_DETAILED_TESTS = '''
# Date		:	''' + SCRIPT_VERSION + '''
description     "PlatformCyclingTest"
author          "Gulavani, Pallavi (pallavi.gulavani@intel.com), Narayan, Nupur (nupur.narayan@intel.com), Panse, Vrukesh V (vrukesh.v.panse@intel.com)"

start on starting system-services

script
  if [ -e /usr/local/PlatformCyclingTest/warm_boot_detailed_tests.py ]; then
    exec /usr/local/bin/python /usr/local/PlatformCyclingTest/warm_boot_detailed_tests.py
  fi
end script
'''

CONF_FILE_ETC_INIT_COLD_BOOT_S5_SUSPEND_RESUME_QUICK_TESTS = '''
# Date		:	''' + SCRIPT_VERSION + '''
description     "PlatformCyclingTest"
author          "Gulavani, Pallavi (pallavi.gulavani@intel.com), Narayan, Nupur (nupur.narayan@intel.com), Panse, Vrukesh V (vrukesh.v.panse@intel.com)"

start on starting system-services

script
  if [ -e /usr/local/PlatformCyclingTest/cold_boot_s5_suspend_resume_quick_tests.py ]; then
    exec /usr/local/bin/python /usr/local/PlatformCyclingTest/cold_boot_s5_suspend_resume_quick_tests.py
  fi
end script
'''

CONF_FILE_ETC_INIT_COLD_BOOT_G3_SUSPEND_RESUME_QUICK_TESTS =  '''
# Date		:	''' + SCRIPT_VERSION + '''
description     "PlatformCyclingTest"
author          "Gulavani, Pallavi (pallavi.gulavani@intel.com), Narayan, Nupur (nupur.narayan@intel.com), Panse, Vrukesh V (vrukesh.v.panse@intel.com)"

start on starting system-services

script
  if [ -e /usr/local/PlatformCyclingTest/cold_boot_g3_suspend_resume_quick_tests.py ]; then
    exec /usr/local/bin/python /usr/local/PlatformCyclingTest/cold_boot_g3_suspend_resume_quick_tests.py
  fi
end script
'''

CONF_FILE_ETC_INIT_WARM_BOOT_SUSPEND_RESUME_QUICK_TESTS = '''
# Date		:	''' + SCRIPT_VERSION + '''
description     "PlatformCyclingTest"
author          "Gulavani, Pallavi (pallavi.gulavani@intel.com), Narayan, Nupur (nupur.narayan@intel.com), Panse, Vrukesh V (vrukesh.v.panse@intel.com)"

start on starting system-services

script
  if [ -e /usr/local/PlatformCyclingTest/warm_boot_suspend_resume_quick_tests.py ]; then
    exec /usr/local/bin/python /usr/local/PlatformCyclingTest/warm_boot_suspend_resume_quick_tests.py
  fi
end script
'''

CONF_FILE_ETC_INIT_COLD_BOOT_G3_WARM_BOOT_QUICK_TESTS = '''
# Date		:	''' + SCRIPT_VERSION + '''
description     "PlatformCyclingTest"
author          "Gulavani, Pallavi (pallavi.gulavani@intel.com), Narayan, Nupur (nupur.narayan@intel.com), Panse, Vrukesh V (vrukesh.v.panse@intel.com)"

start on starting system-services

script
  if [ -e /usr/local/PlatformCyclingTest/cold_boot_g3_warm_boot_quick_tests.py ]; then
    exec /usr/local/bin/python /usr/local/PlatformCyclingTest/cold_boot_g3_warm_boot_quick_tests.py
  fi
end script
'''

""" Create frame object """
frameObj = currentframe()

""" Get current file name """
fileName = str(os.path.basename(__file__))

""" String to track current function name """
functionName = str (__name__)

if os.path.isfile(LOG_FILE):
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": log file present")
else:
	print (str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')) + ": " + fileName + ": line " + str(frameObj.f_lineno) + ": log file does not exist")
