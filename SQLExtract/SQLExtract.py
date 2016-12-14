import os
import re
import datetime
import time


def log(fileName, line):
    f = open(fileName, "a", errors='ignore')
    f.write(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') + " " + line + "\n")
    f.close()

def writeFile(fileName, text):
    f = open(fileName, "a", errors='ignore')
    f.write(text + "\n")
    f.close()

def readFileContents(fileName):
    if(os.path.exists(fileName)):
        f = open(fileName, "r+", errors='ignore')
        return f.read()
    return ""

def extractAllSQLCode(logFile, sourceRoot, resultRoot, dir):
    for root, dirs, files in os.walk(os.path.join(sourceRoot, dir)):
        files = [f for f in files if not f[0] == '.']
        dirs[:] = [d for d in dirs if not d[0] == '.']
        for file in files:
            storeSQLStatements(logFile, os.path.join(root,file), resultRoot, dir)

def storeSQLStatements(logFile, curfile, resultRoot, repoName):
    resultFile = os.path.join(resultRoot, repoName + ".sql")
    contents = readFileContents(curfile)
    result1 = re.search(r'select\s.+\sfrom.+(\s.+)*;', contents, re.IGNORECASE)
    if(result1 != None):
        log(logFile, "regex match: " + result1.group(0))
        writeFile(resultFile, result1.group(0))

    result2 = re.search(r'create\stable\s.+\s*\(.+(\s.+)*;', contents, re.IGNORECASE)
    if(result2 != None):
        log(logFile, "regex match: " + result2.group(0))
        writeFile(resultFile, result2.group(0))

    result3 = re.search(r'insert\sinto\s.+\svalues.+(\s.+)*;', contents, re.IGNORECASE)
    if(result3 != None):
        log(logFile, "regex match: " + result3.group(0))
        writeFile(resultFile, result3.group(0))