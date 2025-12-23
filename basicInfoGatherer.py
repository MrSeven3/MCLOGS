import re
from io import TextIOWrapper

NEOFORGE_LOADER_DETECT_REGEX = r".* \[main\/INFO\] (\[net\.neoforged\.fml\.loading\.moddiscovery\.ModDiscoverer/SCAN\]).*\s*"


def checkLoader(file:TextIOWrapper) -> str:
    loader = ""
    lines = []
    for i, line in enumerate(file):
        if i < 20:
            #print("Loaded line " +str(i) +" with data "+ line)
            lines.append(line)
        else:
            break

    for line in lines:
        if re.match(NEOFORGE_LOADER_DETECT_REGEX,line):
            loader = "Neoforge"
            break

    return loader
