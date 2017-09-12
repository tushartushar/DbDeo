import os
import datetime
import time

def writeFile(fileName, text):
    with open(fileName, "a", errors='ignore') as f:
        f.write(text + "\n")

def readFileContents(fileName):
    if (os.path.exists(fileName)):
        with open(fileName, "r+", errors='ignore') as f:
            return f.read()
    return ""

def log(fileName, line):
    with open(fileName, "a", errors='ignore') as f:
        f.write(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') + " " + line + "\n")
