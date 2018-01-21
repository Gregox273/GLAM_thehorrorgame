# import emotion_api
import analyze
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
            time.sleep(0.001)
            continue
        yield line

if __name__ == '__main__':
    # checks if Amnesia has opened Map01
    username = getpass.getuser()
    print(username)
    #
    # # if os.name == "mac":
    # logfileLocation = ("/Users/" + username + "/Library/Application Support/Frictional Games/Amnesia/Main/hpl.log")
    # # elif os.name == "nt":
    # #     # find logfileLocation on Windows
    # #     logfileLocation = ("")
    # logfile = open(logfileLocation,"r")
    # loglines = follow(logfile)
    # for line in loglines:
    #     print("reading 1")
    #     if " -------- Loading map 'map01_ch1.map' ---------" in line:
    #         print("Recognized: Entering Map 1")
    #         break
    #     elif " -------- Loading complete ---------" in line:
    #         print("Recognized: Loaded Map 1")
    #         break
    # logfile.close()
    # # records images until map03 begins to load
    # #     counter = 1
    # logfile = open(logfileLocation,"r")
    # loglines = follow(logfile)
    # for line in loglines:
    #     print("reading 2")
    #     if "Trigger: Leaving Map 1" in line:
    #         print("Recognized: Leaving Map 1")
    #         break
    #         #     	fileName = "p_" + counter
    #         #     	emotion_simple(fileName)
    #         #     	time.sleep(0.5)
    #         #     	counter += 1
    # logfile.close()

    # gets jumps in fear from each scare
    # fearNums = analyze("p_", counter)
    fearNums = analyze.genFearScores("p", 4)
    fearNums = [int(x * 100) for x in fearNums]
    fearLevels = {'jumpscare':fearNums[0], 'suspense':fearNums[1], 'insanity':fearNums[2], 'monsters':fearNums[3]}
    # fearScale = OrderedDict(sorted(fearLevels.items(), key=itemgetter(1), reverse=True)) # sorts scares by most terrifying to least
    # print(fearScale)

    # appends void getFearLevels() to map03_ch1.hps
    getFearLevels = "void getFearLevels(){"
    rank = 1
    # creates void getFearLevels()
    for scare, fearLevel in fearLevels.items():
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
