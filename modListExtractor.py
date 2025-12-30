import re

def neoforgeModListExtractor(filePath, isCrashReport:bool):
    MOD_LIST_START_REGEX = r"\s*Mod List:\s"
    CRASH_REPORT_MOD_LIST_END_REGEX = r"\s*Crash Report UUID: .*"
    LATEST_LOG_MOD_LIST_END_REGEX = r"\S*.*\[main/\w*\].*"

    modListStartLine = -1
    modListEndLine = -1
    modList:list = []

    #find the bounds of the mod list
    if isCrashReport:
        file = open(filePath, "r", errors="ignore")
        for i,line in enumerate(file):
            if re.match(MOD_LIST_START_REGEX,line):
                modListStartLine = i + 1
                print("Crash report mod list starts at "+str(modListStartLine))
            if re.match(CRASH_REPORT_MOD_LIST_END_REGEX,line) and modListStartLine != -1:
                modListEndLine = i - 1
                print("Crash report mod list ends at "+str(modListEndLine))
                break
        file.close()

        MOD_LIST_DATA_EXTRACT_REGEX = r"\s*(.+?)\s*?\|(.+?)\s*\|([0-9a-z_]+?)\s*?\|([0-9a-zA-Z-.+]+?)\s*?\|Manifest:.*"

        file = open(filePath, "r", errors="ignore")
        for i,line in enumerate(file):
            if modListStartLine <= i <= modListEndLine:
                modList.append(re.findall(MOD_LIST_DATA_EXTRACT_REGEX,line)[0])
        file.close()
    else:
        file = open(filePath, "r", errors="ignore")
        for i,line in enumerate(file):
            if re.match(MOD_LIST_START_REGEX,line):
                modListStartLine = i+1
                print("Log mod list starts at "+str(modListStartLine))
            elif re.match(LATEST_LOG_MOD_LIST_END_REGEX,line)and modListStartLine != -1:
                modListEndLine = i - 1
                print("Log mod list ends at "+str(modListEndLine))
                break
        file.close()
    print(modList)



neoforgeModListExtractor("examples/neoforge_example_crash_report.txt",True)
#neoforgeModListExtractor("examples/latest_neoforge_example.log",False)