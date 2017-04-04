import os
import re

def writeFile(fileName, text):
    with open(fileName, "a", errors='ignore') as f:
        f.write(text + "\n")

def readFileContents(fileName):
    if(os.path.exists(fileName)):
        with open(fileName, "r+", errors='ignore') as f:
            return f.read()
    return ""

def computeAllMetrics(sourceRoot, file, resultFile):
    curfile = os.path.join(sourceRoot, file)
    contents = readFileContents(curfile)
    createStmts, insertStmts, selectStmts, updateStmts, ciStmts = computeMetrics(curfile)

    writeFile(resultFile, file + "," + str(selectStmts) + "," + str(createStmts) + "," + str(insertStmts)
              + "," + str(updateStmts) + "," + str(ciStmts))


def computeMetrics(file):
    selectStmts = 0
    createStmts = 0
    insertStmts = 0
    updateStmts = 0
    ciStmts = 0
    with open(file, "r", errors='ignore') as r:
        for line in r:
            match1 = re.search(
                r'select\s+(\%?\w+(\(\w+\))?|(\w+\()?\*\)?)(\s?,\s?\%?\w+(\(\w+|\*\))?)*\s+from\s+(.+\s?)(where\s.+\s)?\s?(order\sby.+\n)?\s?(group\sby\s\w+)?', line, re.IGNORECASE)
            if match1:
                selectStmts += 1
                continue

            match2 = re.search(r'create\stable\s', line, re.IGNORECASE)
            if match2:
                createStmts += 1
                continue

            match3 = re.search(r'insert\sinto\s\w+\svalues', line, re.IGNORECASE)
            if match3:
                insertStmts += 1
                continue

            match4 = re.findall(r'update\s\w+\sset\s*',
                                line, re.IGNORECASE)
            if match4:
                updateStmts += 1
                continue

            match5 = re.search(r'create\sindex\s',
                         line, re.IGNORECASE)
            if match5:
                ciStmts += 1

    return createStmts, insertStmts, selectStmts, updateStmts, ciStmts

