import time
import os
import getpass
from operator import itemgetter
from collections import OrderedDict

def follow(thefile):
    thefile.seek(0,2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line

if __name__ == '__main__':

    # checks if Amnesia has opened Map01
    username = getpass.getuser()
    print(username)
    # if os.name == "mac":
    logfileLocation = ("/Users/" + username + "/Library/Application Support/Frictional Games/Amnesia/Main/hpl.log")
    # elif os.name == "nt":
    #     # find logfileLocation on Windows
    #     logfileLocation = ("")
    logfile = open(logfileLocation,"r")
    loglines = follow(logfile)
    for line in loglines:
        if "Loading map 'map01_ch1.map" in line:
            print("Loading map 'map01_ch1.map")
            break
    logfile.close()

    # begins recording images

    # gets intervals of biggest jumps in fear from images (1-jumpscare, 2-suspense, 3-insanity, 4-monsters)
    fearLevels = {'jumpscare':0.39, 'suspense':0.69, 'insanity':0.42, 'monsters':0.11} # but this would actually be the intervals dictionary from Anindya
    fearScale = OrderedDict(sorted(fearLevels.items(), key=itemgetter(1), reverse=True)) # sorts scares by most terrifying to least
    print(fearScale)

    # appends void getFearLevels() to map03_ch1.hps
    getFearLevels = "void getFearLevels(){"
    rank = 1
    # creates void getFearLevels()
    for scare, fearLevel in fearScale.items():
        getFearLevels = getFearLevels + "SetGlobalVarInt(\"" + scare + "\"," + str(rank) + ");"
        rank += 1
    getFearLevels += "}"
    print(getFearLevels)
    # if os.name == "mac":
    responsiveMapLocation = "/Users/" + username + "/Library/Application Support/Steam/steamapps/common/Amnesia The Dark Descent/custom_stories/GLAM/maps/map03_ch1.hps"
    # elif os.name == "nt":
    #   responsiveMapLocation = ("")
    with open(responsiveMapLocation, "a") as responsiveMap:
        responsiveMap.write(getFearLevels)