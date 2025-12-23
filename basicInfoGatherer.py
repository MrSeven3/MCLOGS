import re
from io import TextIOWrapper

NEOFORGE_LOADER_DETECT_REGEX = r".*\[main\/INFO\] \[cpw\.mods\.modlauncher\.Launcher\/MODLAUNCHER\]: .* --fml\.neoForgeVersion"

NEOFORGE_LOADER_VERSION_FLAG_EXTRACT_REGEX = r".*\[main\/INFO\] \[cpw\.mods\.modlauncher\.Launcher\/MODLAUNCHER\]: .* --fml\.neoForgeVersion, ([0-9]{2}\.[0-9]{1,2}\.[0-9]{1,3}), "
NEOFORGE_REG_VERSION_FLAG_EXTRACT_REGEX = r".*\[main\/INFO\]: .* --version, ([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}|neoforge-[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})" #gets the version flag. this is either the mc version or the loader version


def checkGameData(file:TextIOWrapper) -> str:
    loader = ""
    loaderVer = ""
    minecraftVer = ""
    javaVer = ""
    for i, line in enumerate(file):
        if i == 0 : #check first line for useful info
            #check if neoforge loader
            if re.match(NEOFORGE_LOADER_DETECT_REGEX,line):
                loader = "Neoforge"

                loaderVer = re.findall(NEOFORGE_LOADER_VERSION_FLAG_EXTRACT_REGEX, line) #detect neoforge loader version
                print("Detected loader is Neoforge, version " +str(loaderVer[0]))

                versionFlagData = re.match(NEOFORGE_REG_VERSION_FLAG_EXTRACT_REGEX, line)
                if versionFlagData[0]

    gameData = {"loader":loader, "loaderVersion":loaderVer, "minecraftVersion":minecraftVer,"javaVersion":javaVer}
    return gameData
