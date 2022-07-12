TO DO:
* Stop_on_error for suspend-resume errors
* Execute in suite mode
* pycodestyle --max-line-length 80 /home/kboginen/chromeautomation/src/third_party/autotest/files/client/common_lib/cros/chromeui_helper.py
* autopep8 --in-place --aggressive --max-line-length 80 * /home/kboginen/chromeautomation/src/third_party/autotest/files/client/common_lib/cros/chromeui_helper.py
* https://www.python.org/dev/peps/pep-0008/
* v4l2 details are not coming:
"array_v4l2=($(v4l2-ctl --list-devices | grep /dev/video | awk -F  ' ' '{print $1}'));for item_v4l2 in ${array_v4l2[@]};do echo $item_v4l2;v4l2-ctl --device=$item_v4l2 --all; done" : "v4l2_info_original.txt",


Known issue:
* Command: "amixer --version" shows None
* Command "i2cdetect -y -r 9" may fail suspend-resume. For debug, remove command and check
* Command "i2cdetect -y -r 15" may fail suspend-resume. For debug, remove command and check

Usage:
(1). Copy the folder PlatformCyclingTest to /usr/local/

(2). Change to directory:
cd /usr/local/PlatformCyclingTest/

(3). Change file permissions:
chmod 0777 *.*

(4). Reboot DUT and without logging, go to Terminal (Ctrl + Alt + F2)
cd /usr/local/PlatformCyclingTest/

(5). Start the tests with syntax command:
python start_tests.py <TestNumber> <NumberOfIterations>
where both <TestNumber> and <NumberOfIterations> must be positive integers

Note: Charger is mandatory for iterations more than 50.

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
10) Run Cold Boot Quick Test (S0-S5) + suspend-resume quick test. Pass parameter for number of iterations for cold boot (S0-S5). Suspend resume iterations are hard-coded.
11) Run Cold Boot Quick Test (S0-S5-G3) + suspend-resume quick test. Pass parameter for number of iterations for cold boot (S0-S5-G3). Suspend resume iterations are hard-coded.
12) Run Warm Boot Quick Test + suspend-resume quick test. Pass parameter for number of iterations for warm boot. Suspend resume iterations are hard-coded.
13) Run Cold Boot Quick Test (S0-S5-G3) + warm boot quick test. Pass parameter for total number of iterations (warm + cold).

<NumberOfIterations> is any number between 3 and 10000.

Example command to disable rootfs verification:
python start_tests.py 1

Example command to run cold boot test from S5 for 1000 iterations
python start_tests.py 3 1000

Example command to run cold boot test from G3 for 1000 iterations
python start_tests.py 4 1000

Example command to run warm boot test for 1000 iterations
python start_tests.py 7 1000

Example command to run suspend-resume for 1000 iterations
python start_tests.py 9 1000

(6). Stop the warm/cold boot tests, by running shell script as below. This is needed even if tests are terminated/completed/interrupted due to any reason:
python stop_tests.py

(7). See the details of error logs in file "/usr/local/stability_logs/platform_error_detailed.log"

(8). See the summary of error logs in file "/usr/local/stability_logs/platform_error_summary.log"

(9). See the time logs in file "/usr/local/stability_logs/cycling_time_log.txt"
