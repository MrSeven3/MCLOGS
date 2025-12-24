import os.path
import sys
import re
import basicInfoGatherer
import time

LOG_EXTENSION_REGEX = r".*\.log|.*\.txt"

print("Welcome to MCLOGS, the Minecraft log analyzer! (yes, that stands for something)")
print("Please enter the path of the log to analyze. In the future, this can be done use a command line argument")
file_path = input()

if not os.path.exists(file_path):
    print("We couldn't find a file at that path")
    print("Please enter a path that is valid")
    time.sleep(3)
    sys.exit(1)


if not re.match(LOG_EXTENSION_REGEX, file_path):
    print("Please enter a file that has the extentions .log or .txt, as they are the only ones that are valid Minecraft log files")
    time.sleep(3)
    sys.exit(1)
else:
    file = open(file_path, "r",errors='ignore')
    data = []
    isCrashReport = False
    if basicInfoGatherer.isCrashReport(file):
        isCrashReport = True

        file.close()
        file = open(file_path, "r", errors='ignore')

        data = basicInfoGatherer.crashReportBasicInfoGatherer(file)
        print("Gathered basic data:")
        print(str(data))
    else:

        file.close()
        file = open(file_path, "r", errors='ignore')

        data = basicInfoGatherer.checkGameVersions(file)
        print("Gathered basic data:")
        print(str(data))
