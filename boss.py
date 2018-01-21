import emotion_api
import analyze
import time
import getpass
from sys import platform
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

    if platform == "linux" or platform == "linux2":
    # linux
        logfileLocation = ("/home/" + username + "/.frictionalgames/Amnesia/Main/hpl.log")
    elif platform == "darwin":
    # OS X
        logfileLocation = ("/Users/" + username + "/Library/Application Support/Frictional Games/Amnesia/Main/hpl.log")
    # elif platform == "win32" or platform == "cygwin":
    # Windows...

    logfile = open(logfileLocation,"r")
    loglines = follow(logfile)
    for line in loglines:
        print("reading 1")
        if " -------- Loading map 'map01_ch1.map' ---------" in line:
            print("Recognized: Entering Map 1")
            break
        elif " -------- Loading complete ---------" in line:
            print("Recognized: Loaded Map 1")
            break
    logfile.close()
    # records images until map03 begins to load
    counter = 1
    logfile = open(logfileLocation,"r")
    loglines = follow(logfile)
    for line in loglines:
        print("reading 2")
        if "Trigger: Leaving Map 1" in line:
            print("Recognized: Leaving Map 1")
            break
        else:
        	fileName = "p_" + counter
        	emotion_api.emotion_simple(fileName)
        	time.sleep(0.5)
        	counter += 1
    logfile.close()

    # gets jumps in fear from each scare
    fearNums = analyze.genFearScores("p_", counter)
    # fearNums = analyze.genFearScores("p", 4)
    fearNums = [int(x * 100) for x in fearNums]
    fearLevels = {'jumpscare':fearNums[0], 'suspense':fearNums[1], 'insanity':fearNums[2], 'monsters':fearNums[3]}
    # fearScale = OrderedDict(sorted(fearLevels.items(), key=itemgetter(1), reverse=True)) # sorts scares by most terrifying to least
    # print(fearScale)

    # appends void getFearLevels() to map03_ch1.hps
    getFearLevels = "void getFearLevels(){"
    # creates void getFearLevels()
    for scare, fearLevel in fearLevels.items():
        getFearLevels = getFearLevels + "SetGlobalVarInt(\"" + scare + "\"," + fearLevel + ");"
    getFearLevels += "}"
    print(getFearLevels)

    if platform == "linux" or platform == "linux2":
    # linux
        responsiveMapLocation = "/home/" + username + "/.local/share/Steam/steamapps/common/Amnesia The Dark Descent/custom_stories/GLAM The Horror Game/maps/map03_ch1.hps"
    elif platform == "darwin":
    # OS X
        responsiveMapLocation = "/Users/" + username + "/Library/Application Support/Steam/steamapps/common/Amnesia The Dark Descent/custom_stories/GLAM/maps/map03_ch1.hps"
    # elif platform == "win32" or platform == "cygwin":
    # Windows...

    with open(responsiveMapLocation, "a") as responsiveMap:
        responsiveMap.write(getFearLevels)
