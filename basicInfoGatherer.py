import re
from io import TextIOWrapper

NEOFORGE_LOADER_DETECT_REGEX = r"\t{2}NeoForge.*"

NEOFORGE_LOADER_VERSION_EXTRACT_REGEX = r"\t{2}NeoForge ([0-9]{1,2}\.[0-9]{1,3}\.[0-9]{1,4}).*"
NEOFORGE_MC_VERSION_EXTRACT_REGEX = r"([0-9]{1,2}\.[0-9]{1,3})\.[0-9]{1,4}" #extracts the minecraft version from the provided neoforge version

def checkGameVersions(file:TextIOWrapper) -> str:
    loader = ""
    loaderVer = ""
    minecraftVer = ""
    javaVer = ""
    for i, line in enumerate(file):
        if i < 700:
            if re.match(NEOFORGE_LOADER_DETECT_REGEX,line):
                loader = "NeoForge"
                loaderVer = re.findall(NEOFORGE_LOADER_VERSION_EXTRACT_REGEX,line)[0]
                print("Detected loader is Neoforge, version " + str(loaderVer))

                minecraftVer = re.findall(NEOFORGE_MC_VERSION_EXTRACT_REGEX,loaderVer)[0]
                minecraftVer = "1." + minecraftVer
                print("Minecraft version is " + str(minecraftVer))


    gameVersions = {"loader":loader, "loaderVersion":loaderVer, "minecraftVersion":minecraftVer}
    return gameVersions
