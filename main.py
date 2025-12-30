import os.path
import sys
import re
import basicInfoGatherer
import time

import extraInfoGatherer
import modListExtractor

LOG_EXTENSION_REGEX = r".*\.log|.*\.txt"

print("Welcome to MCLOGS, the Minecraft log analyzer! (yes, that stands for something)")
print("Please enter the path of the log to analyze. In the future, this can be done use a command line argument")
filePath = input()

if not os.path.exists(filePath):
    print("We couldn't find a file at that path")
    print("Please enter a path that is valid")
    time.sleep(3)
    sys.exit(1)

basicData = {}

if not re.match(LOG_EXTENSION_REGEX, filePath):
    print("Please enter a file that has the extentions .log or .txt, as they are the only ones that are valid Minecraft log files")
    time.sleep(3)
    sys.exit(1)
else:
    print("")
    isCrashReport = False
    if basicInfoGatherer.isCrashReport(filePath):
        isCrashReport = True

        basicData = basicInfoGatherer.crashReportBasicInfoGatherer(filePath)
        improvedCrashReportData = extraInfoGatherer.checkImprovedCrashReports(filePath)
        isSinytraPresent = extraInfoGatherer.checkSinytraConnectorPresence(filePath)
        modList = modListExtractor.neoforgeModListExtractor(filePath, True)


        print("Gathered basic data:")
        print("Loader: " + str(basicData['loader']))
        print("Loader Version: " + str(basicData['loaderVersion']))
        print("Minecraft Version: " + str(basicData['minecraftVersion']))
        print("Is Crash Report: " + str(basicData['isCrashReport']))


        if isSinytraPresent:
            time.sleep(1)
            print("\nWARNING:")
            print("Sinytra Connector has been detected. It is known to have common issues.\nPlease verify that Sinytra Connector and related Fabric mods are not causing the problem")


        if improvedCrashReportData['isImproved']:
            time.sleep(2)

            print("")
            print("------------------------------------------------------------------")
            print("")
            print("Improved Crash Reports found")
            print("The following is data from Improved Crash Reports")
            print("")
            print(str(improvedCrashReportData['improvedReport']))
    else:
        basicData = basicInfoGatherer.checkGameVersions(filePath)
        print("Gathered basic data:")
        print("Loader: " + str(basicData['loader']))
        print("Loader Version: " + str(basicData['loaderVersion']))
        print("Minecraft Version: " + str(basicData['minecraftVersion']))
        print("Is Crash Report: " + str(basicData['isCrashReport']))
