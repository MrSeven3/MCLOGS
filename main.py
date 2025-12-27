import os.path
import sys
import re
import basicInfoGatherer
import time

import extraInfoGatherer

LOG_EXTENSION_REGEX = r".*\.log|.*\.txt"

print("Welcome to MCLOGS, the Minecraft log analyzer! (yes, that stands for something)")
print("Please enter the path of the log to analyze. In the future, this can be done use a command line argument")
file_path = input()

if not os.path.exists(file_path):
    print("We couldn't find a file at that path")
    print("Please enter a path that is valid")
    time.sleep(3)
    sys.exit(1)

basicData = {}

if not re.match(LOG_EXTENSION_REGEX, file_path):
    print("Please enter a file that has the extentions .log or .txt, as they are the only ones that are valid Minecraft log files")
    time.sleep(3)
    sys.exit(1)
else:
    print("")
    isCrashReport = False
    if basicInfoGatherer.isCrashReport(file_path):
        isCrashReport = True

        basicData = basicInfoGatherer.crashReportBasicInfoGatherer(file_path)
        improvedCrashReportData = extraInfoGatherer.checkImprovedCrashReports(file_path)
        isSinytraPresent = extraInfoGatherer.checkSinytraConnectorPresence(file_path)


        print("Gathered basic data:")
        print("Loader: " + str(basicData['loader']))
        print("Loader Version: " + str(basicData['loaderVersion']))
        print("Minecraft Version: " + str(basicData['minecraftVersion']))
        print("Is Crash Report: " + str(basicData['isCrashReport']))

        time.sleep(1)

        if isSinytraPresent:
            print("\nWARNING:")
            print("Sinytra Connector has been detected. It is known to have common issues.\nPlease verify that Sinytra Connector and related Fabric mods are not causing the problem")

        time.sleep(2)

        print("")
        print("------------------------------------------------------------------")
        print("")

        if improvedCrashReportData['isImproved']:
            print("Improved Crash Reports found")
            print("The following is data from Improved Crash Reports")
            print("")
            print(str(improvedCrashReportData['improvedReport']))
    else:
        basicData = basicInfoGatherer.checkGameVersions(file_path)
        print("Gathered basic data:")
        print("Loader: " + str(basicData['loader']))
        print("Loader Version: " + str(basicData['loaderVersion']))
        print("Minecraft Version: " + str(basicData['minecraftVersion']))
        print("Is Crash Report: " + str(basicData['isCrashReport']))
