import re
from io import TextIOWrapper

NEOFORGE_LOADER_DETECT_REGEX = r"\t{2}NeoForge.*"

NEOFORGE_LOADER_VERSION_EXTRACT_REGEX = r"\t{2}NeoForge ([0-9]{1,2}\.[0-9]{1,3}\.[0-9]{1,4}).*"
NEOFORGE_MC_VERSION_EXTRACT_REGEX = r"([0-9]{1,2}\.[0-9]{1,3})\.[0-9]{1,4}" #extracts the minecraft version from the provided neoforge version


FABRIC_LOADER_DETECT_REGEX = r".* \[main\/INFO\]: Loading Minecraft [0-9]\.[0-9]{1,2}\.[0-9]{1,2} with Fabric Loader [0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,2}.*"

FABRIC_LOADER_VERSION_EXTRACT_REGEX = r".* \[main\/INFO\]: Loading Minecraft [0-9]\.[0-9]{1,2}\.[0-9]{1,2} with Fabric Loader ([0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,2}).*"
FABRIC_MC_VERSION_EXTRACT_REGEX = r".* \[main\/INFO\]: Loading Minecraft ([0-9]\.[0-9]{1,2}\.[0-9]{1,2}) with Fabric Loader [0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,2}.*"


QUILT_LOADER_DETECT_REGEX = r".* \[main\/INFO\]: Loading Minecraft [0-9]\.[0-9]{1,2}\.[0-9]{1,2} with Quilt Loader [0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,2}.*"

QUILT_LOADER_VERSION_EXTRACT_REGEX = r".* \[main\/INFO\]: Loading Minecraft [0-9]\.[0-9]{1,2}\.[0-9]{1,2} with Quilt Loader ([0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,2}).*"
QUILT_MC_VERSION_EXTRACT_REGEX = r".* \[main\/INFO\]: Loading Minecraft ([0-9]\.[0-9]{1,2}\.[0-9]{1,2}) with Quilt Loader [0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,2}.*"


FORGE_LOADER_DETECT_REGEX = r".*\[main\/INFO\].*: ModLauncher running.* --fml.forgeVersion, [0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,2}"

FORGE_LOADER_VERSION_EXTRACT_REGEX = r".*\[main\/INFO\].*: ModLauncher running.* --fml.forgeVersion, ([0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,2})"
FORGE_MC_VERSION_EXTRACT_REGEX = r".*\[main\/INFO\].*: ModLauncher running.* --fml.mcVersion, ([0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,2})"

def checkGameVersions(file:TextIOWrapper) -> str:
    loader = ""
    loaderVer = ""
    minecraftVer = ""
    for i, line in enumerate(file):
        if i < 700:
            if re.match(NEOFORGE_LOADER_DETECT_REGEX,line): #neoforge detection
                loader = "NeoForge"
                loaderVer = re.findall(NEOFORGE_LOADER_VERSION_EXTRACT_REGEX,line)[0] #neoforge version extration
                print("Detected loader is Neoforge, version " + str(loaderVer))

                minecraftVer = re.findall(NEOFORGE_MC_VERSION_EXTRACT_REGEX,loaderVer)[0] #mc version extraction
                minecraftVer = "1." + minecraftVer
                print("Minecraft version is " + str(minecraftVer))
                break

            elif re.match(FABRIC_LOADER_DETECT_REGEX,line) and i == 0: #fabric loader detection
                loader = "Fabric"
                loaderVer = re.findall(FABRIC_LOADER_VERSION_EXTRACT_REGEX,line)[0]
                print("Loader is Fabric version " + str(loaderVer))

                minecraftVer = re.findall(FABRIC_MC_VERSION_EXTRACT_REGEX,line)[0]
                print("Minecraft is version " + str(minecraftVer))
                break

            elif re.match(QUILT_LOADER_DETECT_REGEX,line) and i == 0: #quilt loader detection
                loader = "Quilt"
                loaderVer = re.findall(QUILT_LOADER_VERSION_EXTRACT_REGEX,line)[0]
                print("Loader is Quilt version " + str(loaderVer))

                minecraftVer = re.findall(QUILT_MC_VERSION_EXTRACT_REGEX,line)[0]
                print("Minecraft is version " + str(minecraftVer))
                break

            elif re.match(FORGE_LOADER_DETECT_REGEX,line) and i == 0: #forge loader detection TODO: make this reliable, it may not always detect forge
                loader = "Forge"
                loaderVer = re.findall(FORGE_LOADER_VERSION_EXTRACT_REGEX,line)[0]
                print("Loader is Forge version " + str(loaderVer))

                minecraftVer = re.findall(FORGE_MC_VERSION_EXTRACT_REGEX,line)[0]
                print("Minecraft is version " + str(minecraftVer))

    gameVersions = {"loader":loader, "loaderVersion":loaderVer, "minecraftVersion":minecraftVer}
    return gameVersions

