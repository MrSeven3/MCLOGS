import re
import time


LOG_EXTENSION_REGEX = "[a-zA-Z0-9]+\.log|txt"

print("Welcome to MCLOGS, the Minecraft log analyzer! (yes, that stands for something)")
print("Please enter the path of the log to analyze. In the future, this can be done use a command line argument")
file_path = input()

if not re.match(LOG_EXTENSION_REGEX, file_path):
    print("Please enter a file that has the extentions .log or .txt, as they are the only ones that are valid Minecraft log files")
else:
    file = open(file_path, "r")
