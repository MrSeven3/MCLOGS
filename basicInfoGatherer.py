import re
from io import TextIOWrapper

def isCrashReport(file:TextIOWrapper) -> bool: #checks if the provided file is a crash report or not
    CRASH_REPORT_DETECT_REGEX = r"-+|=+"

    for i, line in enumerate(file):
        if i == 0 and re.match(CRASH_REPORT_DETECT_REGEX,line):
            return True
        else:
            return False
    return False

def crashReportBasicInfoGatherer(file:TextIOWrapper):
    QUILT_LOADER_DETECT_REGEX = r"---- Quilt Loader: .* ----"
    QUILT_LOADER_VERSION_EXTRACT_REGEX = r"\| Quilt Loader\s*\| quilt_loader\s*\| ([0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,2})\s*.*"
    QUILT_MC_VERSION_EXTRACT_REGEX = r"\| Minecraft\s*\| minecraft\s*\| ([0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,2})\s*.*"

    FABRIC_LOADER_DETECT_REGEX = r"\s*fabricloader: Fabric Loader [0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,2}"
    FABRIC_LOADER_VERSION_EXTRACT_REGEX = r"\s*fabricloader: Fabric Loader ([0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,2})"
    FABRIC_MC_VERSION_EXTRACT_REGEX = r"\s*minecraft: Minecraft ([0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,2})"

    NEOFORGE_LOADER_DETECT_REGEX = r"\s*neoforge-[0-9]{1,2}\.[0-9]{1,3}\.[0-9]{1,4}-.*\.jar\s*\|NeoForge\s*\|neoforge\s*\|[0-9]{1,2}\.[0-9]{1,3}\.[0-9]{1,4}\s*\|Manifest.*"
    NEOFORGE_LOADER_VERSION_EXTRACT_REGEX = r"\s*neoforge-([0-9]{1,2}\.[0-9]{1,3}\.[0-9]{1,4})-.*\.jar\s*\|NeoForge\s*\|neoforge\s*\|[0-9]{1,2}\.[0-9]{1,3}\.[0-9]{1,4}\s*\|Manifest.*"
    NEOFORGE_MC_VERSION_EXTRACT_REGEX = r"([0-9]{1,2}\.[0-9]{1,3})\.[0-9]{1,4}"  # extracts the minecraft version from the provided neoforge version

    FORGE_LOADER_DETECT_REGEX = r"\s*forge.*\.jar\s*\|Forge\s*\|forge\s*\|[0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,2}\s*\|.*"
    FORGE_LOADER_VERSION_EXTRACT_REGEX = r"\s*forge.*\.jar\s*\|Forge\s*\|forge\s*\|([0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,2})\s*\|.*"
    FORGE_MC_VERSION_EXTRACT_REGEX = r"\s*client-[0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,2}-[0-9]*\.*[0-9]*.*\.jar\s*\|Minecraft\s*\|minecraft\s*\|([0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,2}).*"

    loader = ""
    loaderVer = ""
    minecraftVer = ""
    for i,line in enumerate(file):
        if i < 200 and re.match(QUILT_LOADER_DETECT_REGEX, line):# quilt detection
            loader = "Quilt"
        if loader == "Quilt": #extra quilt data gathering
            if re.match(QUILT_MC_VERSION_EXTRACT_REGEX,line):
                minecraftVer = re.findall(QUILT_MC_VERSION_EXTRACT_REGEX,line)[0]#find the mod listed as "minecraft" and get its version
            if re.match(QUILT_LOADER_VERSION_EXTRACT_REGEX,line):
                loaderVer = re.findall(QUILT_LOADER_VERSION_EXTRACT_REGEX,line)[0]#find the mod listed as "quilt loader" and get its version

        if re.match(FABRIC_LOADER_DETECT_REGEX,line): #fabric detection
            loader = "Fabric"
            loaderVer = re.findall(FABRIC_LOADER_VERSION_EXTRACT_REGEX,line)[0]#find the mod listed as "fabric loader" and get its version
        if loader == "Fabric" and re.match(FABRIC_MC_VERSION_EXTRACT_REGEX,line): #extra fabric data gathering
            minecraftVer = re.findall(FABRIC_MC_VERSION_EXTRACT_REGEX,line)[0]#find the mod listed as "minecraft" and get its version

        if re.match(NEOFORGE_LOADER_DETECT_REGEX,line):#neoforge detection
            loader = "NeoForge"
            loaderVer = re.findall(NEOFORGE_LOADER_VERSION_EXTRACT_REGEX,line)[0] #get the neoforge version from the modlist
            minecraftVer = "1." + re.findall(NEOFORGE_MC_VERSION_EXTRACT_REGEX,loaderVer)[0] # get the minecraft version from the neoforge version

        if re.match(FORGE_LOADER_DETECT_REGEX,line):
            loader = "Forge"
            loaderVer = re.findall(FORGE_LOADER_VERSION_EXTRACT_REGEX,line)[0]
        if minecraftVer == "" and re.match(FORGE_MC_VERSION_EXTRACT_REGEX,line):
            minecraftVer = re.findall(FORGE_MC_VERSION_EXTRACT_REGEX,line)[0]


    if loader == '':
        print("It appears you are playing vanilla, or you are using an unsupported modloader. Detection and analysis will continue as though your game is vanilla, but it may not be correct.")
        loader = "Vanilla"
    gameVersions = {"loader": loader, "loaderVersion": loaderVer, "minecraftVersion": minecraftVer,"isCrashReport":True}
    return gameVersions

def checkGameVersions(file:TextIOWrapper): #gets all basic versions from a log file, including modloader, modloader version, and minecraft version
    NEOFORGE_LOADER_DETECT_REGEX = r"\t{2}NeoForge.*"
    NEOFORGE_LOADER_VERSION_EXTRACT_REGEX = r"\t{2}NeoForge ([0-9]{1,2}\.[0-9]{1,3}\.[0-9]{1,4}).*"
    NEOFORGE_MC_VERSION_EXTRACT_REGEX = r"([0-9]{1,2}\.[0-9]{1,3})\.[0-9]{1,4}"  # extracts the minecraft version from the provided neoforge version

    FABRIC_LOADER_DETECT_REGEX = r".* \[main\/INFO\]: Loading Minecraft [0-9]\.[0-9]{1,2}\.[0-9]{1,2} with Fabric Loader [0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,2}.*"
    FABRIC_LOADER_VERSION_EXTRACT_REGEX = r".* \[main\/INFO\]: Loading Minecraft [0-9]\.[0-9]{1,2}\.[0-9]{1,2} with Fabric Loader ([0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,2}).*"
    FABRIC_MC_VERSION_EXTRACT_REGEX = r".* \[main\/INFO\]: Loading Minecraft ([0-9]\.[0-9]{1,2}\.[0-9]{1,2}) with Fabric Loader [0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,2}.*"

    QUILT_LOADER_DETECT_REGEX = r".* \[main\/INFO\]: Loading Minecraft [0-9]\.[0-9]{1,2}\.[0-9]{1,2} with Quilt Loader [0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,2}.*"
    QUILT_LOADER_VERSION_EXTRACT_REGEX = r".* \[main\/INFO\]: Loading Minecraft [0-9]\.[0-9]{1,2}\.[0-9]{1,2} with Quilt Loader ([0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,2}).*"
    QUILT_MC_VERSION_EXTRACT_REGEX = r".* \[main\/INFO\]: Loading Minecraft ([0-9]\.[0-9]{1,2}\.[0-9]{1,2}) with Quilt Loader [0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,2}.*"

    FORGE_LOADER_DETECT_REGEX = r".*\[main\/INFO\].*: ModLauncher running.* --fml.forgeVersion, [0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,2}"
    FORGE_LOADER_VERSION_EXTRACT_REGEX = r".*\[main\/INFO\].*: ModLauncher running.* --fml.forgeVersion, ([0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,2})"
    FORGE_MC_VERSION_EXTRACT_REGEX = r".*\[main\/INFO\].*: ModLauncher running.* --fml.mcVersion, ([0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,2})"

    loader = ""
    loaderVer = ""
    minecraftVer = ""
    for i, line in enumerate(file):
        if i < 700:
            if re.match(NEOFORGE_LOADER_DETECT_REGEX,line): #neoforge detection
                loader = "NeoForge"
                loaderVer = re.findall(NEOFORGE_LOADER_VERSION_EXTRACT_REGEX,line)[0] #neoforge version extration
                #print("Detected loader is Neoforge, version " + str(loaderVer))

                minecraftVer = re.findall(NEOFORGE_MC_VERSION_EXTRACT_REGEX,loaderVer)[0] #mc version extraction
                minecraftVer = "1." + minecraftVer
                #print("Minecraft version is " + str(minecraftVer))
                break

            elif re.match(FABRIC_LOADER_DETECT_REGEX,line) and i == 0: #fabric loader detection
                loader = "Fabric"
                loaderVer = re.findall(FABRIC_LOADER_VERSION_EXTRACT_REGEX,line)[0]
                #print("Loader is Fabric version " + str(loaderVer))

                minecraftVer = re.findall(FABRIC_MC_VERSION_EXTRACT_REGEX,line)[0]
                #print("Minecraft is version " + str(minecraftVer))
                break

            elif re.match(QUILT_LOADER_DETECT_REGEX,line) and i == 0: #quilt loader detection
                loader = "Quilt"
                loaderVer = re.findall(QUILT_LOADER_VERSION_EXTRACT_REGEX,line)[0]
                #print("Loader is Quilt version " + str(loaderVer))

                minecraftVer = re.findall(QUILT_MC_VERSION_EXTRACT_REGEX,line)[0]
                #print("Minecraft is version " + str(minecraftVer))
                break

            elif re.match(FORGE_LOADER_DETECT_REGEX,line) and i == 0: #forge loader detection TODO: make this reliable, it may not always detect forge
                loader = "Forge"
                loaderVer = re.findall(FORGE_LOADER_VERSION_EXTRACT_REGEX,line)[0]
                #print("Loader is Forge version " + str(loaderVer))

                minecraftVer = re.findall(FORGE_MC_VERSION_EXTRACT_REGEX,line)[0]
                #print("Minecraft is version " + str(minecraftVer))

    if loader == '':
        print("It appears you are playing vanilla, or you are using an unsupported modloader. Detection and analysis will continue as though your game is vanilla, but it may not be correct.")
        print("It is also possible that you are using Forge, which does not have a consistent detection method in regular log files.")
        loader = "Vanilla"
    gameVersions = {"loader":loader, "loaderVersion":loaderVer, "minecraftVersion":minecraftVer,"isCrashReport":False}
    return gameVersions

