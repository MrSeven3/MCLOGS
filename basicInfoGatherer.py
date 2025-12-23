import re
from io import TextIOWrapper

NEOFORGE_LOADER_DETECT_REGEX = r".*\[main\/INFO\] \[cpw\.mods\.modlauncher\.Launcher\/MODLAUNCHER\]: .* --fml\.neoForgeVersion"

NEOFORGE_LOADER_VERSION_FLAG_EXTRACT_REGEX = r".*\[main\/INFO\] \[cpw\.mods\.modlauncher\.Launcher\/MODLAUNCHER\]: .* --fml\.neoForgeVersion, ([0-9]{2}\.[0-9]{1,2}\.[0-9]{1,3}), "
NEOFORGE_MC_VERSION_EXTRACT_REGEX = r"([0-9]{1,2}\.[0-9]{1,2})\.[0-9]{1,4}" #extracts the minecraft version from the provided neoforge version
NEOFORGE_JAVA_VERSION_LINE_DETECT_REGEX = r".*\[main\/INFO\].*: ModLauncher.+ java version "
NEOFORGE_JAVA_VERSION_EXTRACT_REGEX= r".*\[main\/INFO\].*: ModLauncher.+ java version ([0-9]{1,2})\.[0-9]{1,3}\.[0-9]{1,3} by .*"

def checkGameVersions(file:TextIOWrapper) -> str:
    loader = ""
    loaderVer = ""
    minecraftVer = ""
    javaVer = ""
    for i, line in enumerate(file):
        if i == 0 : #check first line for useful info
            #check if neoforge loader
            if re.match(NEOFORGE_LOADER_DETECT_REGEX,line):
                loader = "Neoforge"

                loaderVer = re.findall(NEOFORGE_LOADER_VERSION_FLAG_EXTRACT_REGEX, line)[0] #detect neoforge loader version
                print("Detected loader is Neoforge, version " +str(loaderVer))

                minecraftVer = re.findall(NEOFORGE_MC_VERSION_EXTRACT_REGEX,loaderVer)[0]
                minecraftVer = "1." + minecraftVer
                print("Minecraft version is " + str(minecraftVer))

        if i < 5:
            #run extra info gathering for neoforge
            if loader == "Neoforge":
                if re.match(NEOFORGE_JAVA_VERSION_LINE_DETECT_REGEX,line):
                    javaVer = re.findall(NEOFORGE_JAVA_VERSION_EXTRACT_REGEX, line)[0]
                    print("Running Major Java version " +str(javaVer))


    gameVersions = {"loader":loader, "loaderVersion":loaderVer, "minecraftVersion":minecraftVer,"javaVersion":javaVer}
    return gameVersions
