import os
import datetime
import time

def writeFile(fileName, text):
   try:
     with open(fileName, "a", errors='ignore') as f:
        f.write(text + "\n")
   except:
     print("Exepction while writing file.")
     pass

def readFileContents(fileName):
   try:
     if (os.path.exists(fileName)):
        with open(fileName, "r+", errors='ignore') as f:
            return f.read()
   except:
     print("Exception occurred while reading file.")
     pass
   return ""

def log(fileName, line):
    try:
      with open(fileName, "a", errors='ignore') as f:
        f.write(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') + " " + line + "\n")
    except:
      pass
