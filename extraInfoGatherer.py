import re

def extractImprovedCrashReportsData(file_path) -> str:
    IMPROVED_CRASH_REPORT_START_DETECT_REGEX = r"=+.*Improved Crash Reports.*=+"
    IMPROVED_CRASH_REPORT_END_DETECT_REGEX = r"=+"

    IMPROVED_CRASH_REPORT_DATA_EXTRACT_REGEX= r" (.*)"

    isImprovedCrashReport = False
    crashReportEndLine:int = None
    improvedCrashReportData:str = ""

    file = open(file_path, "r", errors="ignore")
    for i,line in enumerate(file): #detect size of improved crash report:
        if i == 0 and re.match(IMPROVED_CRASH_REPORT_START_DETECT_REGEX,line):
            isImprovedCrashReport = True
        elif isImprovedCrashReport and re.match(IMPROVED_CRASH_REPORT_END_DETECT_REGEX,line):
            crashReportEndLine = i
            break
    file.close()

    file = open(file_path, "r", errors="ignore")
    for i,line in enumerate(file):
        if 1 <= i < crashReportEndLine and line != "\n":
            improvedCrashReportData = improvedCrashReportData + re.findall(IMPROVED_CRASH_REPORT_DATA_EXTRACT_REGEX,line)[0] + "\n"
    file.close()

    return improvedCrashReportData

def checkImprovedCrashReports(file_path) -> dict:
    IMPROVED_CRASH_REPORT_DETECT_REGEX = r"=+.*Improved Crash Reports.*=+"

    file = open(file_path, "r", errors="ignore")
    for i,line in enumerate(file):
        if i == 0 and re.match(IMPROVED_CRASH_REPORT_DETECT_REGEX,line):
            improvedReport = extractImprovedCrashReportsData(file_path)

            file.close()
            return {"isImproved":True,"improvedReport":improvedReport}
        else:
            file.close()
            return {"isImproved":False,"improvedReport":None}

print(str(checkImprovedCrashReports("examples/neoforge_example_crash_report.txt")))

class TestImprovedCrashReports:
    def testCheckImprovedCrash(self): #should detect an improved crash
        result = checkImprovedCrashReports("examples/neoforge_example_crash_report.txt")
        assert result['isImproved'] == True
        assert result['improvedReport'] != "" or result['improvedReport'] is not None
    def testCheckImprovedCrash_NotPresent(self): #shouldn't detect an improved crash
        result = checkImprovedCrashReports("examples/fabric_example_crash_report.txt")
        assert result['isImproved'] == False
        assert result['improvedReport'] is None