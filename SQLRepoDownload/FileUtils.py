import datetime
import time
import os

def log(fileName, line):
    f = open(fileName, "a", errors='ignore')
    f.write(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') + " " + line + "\n")
    f.close()

def readFileContents(fileName):
    if(os.path.exists(fileName)):
        try:
          f = open(fileName, "r+", errors='ignore')
          return f.read()
        except IOError:
          return ""
