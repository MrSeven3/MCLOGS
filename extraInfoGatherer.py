import re

def extractImprovedCrashReportsData(filePath) -> str:
    IMPROVED_CRASH_REPORT_START_DETECT_REGEX = r"=+.*Improved Crash Reports.*=+"
    IMPROVED_CRASH_REPORT_END_DETECT_REGEX = r"=+"

    IMPROVED_CRASH_REPORT_DATA_EXTRACT_REGEX= r" (.*)"

    isImprovedCrashReport = False
    crashReportEndLine:int = None
    improvedCrashReportData:str = ""

    file = open(filePath, "r", errors="ignore")
    for i,line in enumerate(file): #detect size of improved crash report:
        if i == 0 and re.match(IMPROVED_CRASH_REPORT_START_DETECT_REGEX,line):
            isImprovedCrashReport = True
        elif isImprovedCrashReport and re.match(IMPROVED_CRASH_REPORT_END_DETECT_REGEX,line):
            crashReportEndLine = i
            break
    file.close()

    file = open(filePath, "r", errors="ignore")
    for i,line in enumerate(file):
        if 1 <= i < crashReportEndLine and line != "\n":
            improvedCrashReportData = improvedCrashReportData + re.findall(IMPROVED_CRASH_REPORT_DATA_EXTRACT_REGEX,line)[0] + "\n"
    file.close()

    return improvedCrashReportData

def checkImprovedCrashReports(filePath) -> dict:
    IMPROVED_CRASH_REPORT_DETECT_REGEX = r"=+.*Improved Crash Reports.*=+"

    file = open(filePath, "r", errors="ignore")
    for i,line in enumerate(file):
        if i == 0 and re.match(IMPROVED_CRASH_REPORT_DETECT_REGEX,line):
            improvedReport = extractImprovedCrashReportsData(filePath)

            file.close()
            return {"isImproved":True,"improvedReport":improvedReport}
        else:
            file.close()
            return {"isImproved":False,"improvedReport":None}
    return None

def checkSinytraConnectorPresence(filePath) -> bool:
    SINYTRA_CONNECTOR_STRING = "SINYTRA CONNECTOR IS PRESENT!\n"

    file = open(filePath, "r", errors="ignore")
    for i,line in enumerate(file):
        if line == SINYTRA_CONNECTOR_STRING:
            return True
    return False


class TestImprovedCrashReports:
    def testCheckImprovedCrash_Present(self): #should detect an improved crash
        result = checkImprovedCrashReports("examples/neoforge_example_crash_report.txt")
        assert result['isImproved'] == True
        assert result['improvedReport'] != "" or result['improvedReport'] is not None
    def testCheckImprovedCrash_NotPresent(self): #shouldn't detect an improved crash
        result = checkImprovedCrashReports("examples/fabric_example_crash_report.txt")
        assert result['isImproved'] == False
        assert result['improvedReport'] is None
class TestSinytraConnectorPresence:
    def testCheckSinytraConnectorPresence_Present(self):
        result = checkSinytraConnectorPresence("examples/neoforge_example_crash_report.txt")
        assert result == True
    def testCheckSinytraConnectorPresence_NotPresent(self):
        result = checkSinytraConnectorPresence("examples/forge_example_crash_report.txt")
        assert result == False