import os
import re
import FileUtils

def IsRepoHaveSQLCode(folderPath, logFile):
    for root, dirs, files in os.walk(folderPath):
        files = [f for f in files if not f[0] == '.']
        dirs[:] = [d for d in dirs if not d[0] == '.']
        for file in files:
            try:
                if(AreSQLStatementsPresent(logFile, os.path.join(root,file))):
                    FileUtils.log(logFile, "Repo has SQL code")
                    return True
            except:
                print("Exception occurred")
                pass
    FileUtils.log(logFile, "Repo does not have SQL code")
    return False

def AreSQLStatementsPresent(logFile, file):
    contents = FileUtils.readFileContents(file)
    result1 = re.search(r'select\s.+\sfrom', contents, re.IGNORECASE)
    if(result1 != None):
        FileUtils.log(logFile, "regex match: " + result1.group(0))
        return True
    #result2 = re.search(r'create', contents, re.IGNORECASE)
    result2 = re.search(r'create\stable\s.+\s*\(', contents, re.IGNORECASE)
    if(result2 != None):
        FileUtils.log(logFile, "regex match: " + result2.group(0))
        return True
    result3 = re.search(r'insert\sinto\s.+\svalues', contents, re.IGNORECASE)
    if(result3 != None):
        FileUtils.log(logFile, "regex match: " + result3.group(0))
        return True
    return False

