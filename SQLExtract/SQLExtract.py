
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
    lines = set() #using set to eliminate duplicate sql statements
    for root, dirs, files in os.walk(os.path.join(sourceRoot, dir)):
        files = [f for f in files if not f[0] == '.']
        dirs[:] = [d for d in dirs if not d[0] == '.']
        for file in files:
            print("Analyzing file " + str(root) + str(file))
            storeSQLStatements(logFile, os.path.join(root,file), resultRoot, dir, lines)
    resultFile = os.path.join(resultRoot, dir + ".sql")
    f = open(resultFile, "a", errors='ignore')
    for text in lines:
        f.write(text + "\n")
    f.close()

def storeSQLStatements(logFile, curfile, resultRoot, repoName, lines):
    resultFile = os.path.join(resultRoot, repoName + ".sql")
    contents = readFileContents(curfile)

    for m in re.finditer(r'select\s+.+\s+from\s+(.+\s?)(where\s.+\s)?\s?(order\sby.+\n)?("|;)', contents, re.IGNORECASE):
        query = m.group(0).replace("\n", "")
        log(logFile, "regex match: " + query)
        #writeFile(resultFile, query)
        lines.add(query)

    for m in re.finditer(r'create\stable\s.+\s*\((.+?\s*)*?(;|")', contents, re.IGNORECASE + re.MULTILINE):
        query = m.group(0).replace("\n", "")
        log(logFile, "regex match: " + query)
        #writeFile(resultFile, query)
        lines.add(query)

    for m in re.finditer(r'insert\sinto\s\w+\svalues\s*(.+?\s*)*?(;|")', contents, re.IGNORECASE + re.MULTILINE):
        query = m.group(0).replace("\n", "")
        log(logFile, "regex match: " + query)
        #writeFile(resultFile, query)
        lines.add(query)

    for m in re.finditer(r'update\s\w+\sset\s*(\w+?\s*)*?(where\s*(.+?))("|;)', contents, re.IGNORECASE + re.MULTILINE):
        query = m.group(0).replace("\n", "")
        log(logFile, "regex match: " + query)
        #writeFile(resultFile, query)
        lines.add(query)

    for m in re.finditer(r'create\sindex\s\w+\son\s*(.+?\s*)*?("|;)', contents, re.IGNORECASE + re.MULTILINE):
        query = m.group(0).replace("\n", "")
        log(logFile, "regex match: " + query)
        #writeFile(resultFile, query)
        lines.add(query)
