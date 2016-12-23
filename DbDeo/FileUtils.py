import os
import datetime
import time

def writeFile(fileName, text):
    f = open(fileName, "a", errors='ignore')
    f.write(text + "\n")
    f.close()

def readFileContents(fileName):
    if(os.path.exists(fileName)):
        f = open(fileName, "r+", errors='ignore')
        return f.read()
    return ""

def log(fileName, line):
    f = open(fileName, "a", errors='ignore')
    f.write(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') + " " + line + "\n")
    f.close()