import os
import re


def writeFile(fileName, text):
    f = open(fileName, "a", errors='ignore')
    f.write(text + "\n")
    f.close()

def readFileContents(fileName):
    if(os.path.exists(fileName)):
        f = open(fileName, "r+", errors='ignore')
        return f.read()
    return ""

def computeAllMetrics(sourceRoot, file, resultFile):
    curfile = os.path.join(sourceRoot, file)
    contents = readFileContents(curfile)
    createStmts, insertStmts, selectStmts = computeMetrics(contents)

    writeFile(resultFile, file + "," + str(selectStmts) + "," + str(createStmts) + "," + str(insertStmts))


def computeMetrics(contents):
    result1 = re.findall(
        r'(select\s+.+\s+from\s+(.+\s?)(where\s.+\s)?\s?(order\sby.+\n)?;)|("select\s+.+\s+from\s+(.+\s?)(where\s.+\s)?\s?(order\sby.+\n)?")',
        contents, re.IGNORECASE)
    selectStmts = 0
    if (result1 != None):
        selectStmts = len(result1)
    createStmts = 0
    result2 = re.findall(r'(create\stable\s.+\s*\(.+(\s.+)*;)|("create\stable\s.+\s*\(.+(\s.+)*")', contents,
                         re.IGNORECASE)
    if (result2 != None):
        createStmts = len(result2)
    insertStmts = 0
    result3 = re.findall(r'("insert\sinto\s\w+\svalues\s*(.+?\n?)*?")|(insert\sinto\s\w+\svalues\s*(.+?\n?)*?;)',
                         contents, re.IGNORECASE)
    if (result3 != None):
        insertStmts = len(result3)
    return createStmts, insertStmts, selectStmts