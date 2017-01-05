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
    createStmts, insertStmts, selectStmts, updateStmts, ciStmts = computeMetrics(contents)

    writeFile(resultFile, file + "," + str(selectStmts) + "," + str(createStmts) + "," + str(insertStmts)
              + "," + str(updateStmts) + "," + str(ciStmts))


def computeMetrics(contents):
    result1 = re.findall(
        r'("select\s+.+\s+from\s+(.+\s?)(where\s.+\s)?\s?(order\sby.+\n)?")|(select\s+.+\s+from\s+(.+\s?)(where\s.+\s)?\s?(order\sby.+\n)?;)',
        contents, re.IGNORECASE)
    selectStmts = 0
    if (result1 != None):
        selectStmts = len(result1)
    createStmts = 0
    result2 = re.findall(r'create\stable\s.+?\s*\(.+?(;|")', contents,
                         re.IGNORECASE| re.DOTALL)
    if (result2 != None):
        createStmts = len(result2)
    insertStmts = 0
    result3 = re.findall(r'insert\sinto\s\w+\svalues\s*.+?(;|")',
                         contents, re.IGNORECASE| re.DOTALL)
    if (result3 != None):
        insertStmts = len(result3)
    updateStmts = 0
    result4 = re.findall(r'update\s\w+\sset\s*.+?\s*where\s*.+?("|;)',
                         contents, re.IGNORECASE| re.DOTALL)
    if (result4 != None):
        updateStmts = len(result4)
    ciStmts = 0
    result5 = re.findall(r'create\sindex\s\w+\son\s*.+?("|;)',
                         contents, re.IGNORECASE| re.DOTALL)
    if (result5 != None):
        ciStmts = len(result5)

    return createStmts, insertStmts, selectStmts, updateStmts, ciStmts

