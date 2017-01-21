# This program cleanse the extracted sql statements.
# In the first phase of sql statement extraction, we get a lot of noise because regex are not capable of covering all
# variations of sql statements.
# In this phase, we further cleanse the sql statements that we got from the first phase.
import os
from Model import SQLParse
from Model.SQLStmtType import SQLStmtType
import re

repoStoreRoot = "/Users/Tushar/Documents/Research/dbSmells/dbSmellData/resultRepos"
newRepoStoreRoot = "/Users/Tushar/Documents/Research/dbSmells/dbSmellData/resultReposCleansed"


def cleanseCreateTable(parsedStmt):
    count = 0
    newline = ""
    bracket_seen = False
    for token in parsedStmt.flatten():
        if token.value == '(':
            count += 1
            bracket_seen = True
        elif token.value == ')':
            count -= 1
            if count <= 0:
                newline += token.value
                if bracket_seen:
                    return newline
                else:
                    return ""
        newline += token.value
    if bracket_seen:
        return newline
    else:
        return ""


def cleanseSelectStmt(line):
    regex = r'select\s+(\%?\w+(\(\w+\))?|(\w+\()?\*\)?)(\s?,\s?\%?\w+(\(\w+|\*\))?)*\s+from\s+(.+\s?)(where\s.+\s)?\s?(order\sby.+\n)?\s?(group\sby\s\w+)?'
    match = re.search(regex, line, flags=re.IGNORECASE)
    if match:
        return str(match.group(0))
    return ""


def cleanseUpdateStatement(line):
    #It's taking too much time
    #regex = r'update\s\w+\sset\s*[\",\s\']*\s*\w+:*\w*\s*=\s*[\'\":\\]*\s*(\w+:*\w*|\(?\?\)?|\%\w+:*\w*|\$\w+:*\w*)\s*[\'\"\\]*(\s*[\+\-\*\/]\s*\d+)?(\s*,[\",\s\'\\]*\w+:*\w*\s*=\s*[\'\":\\]*\s*(\w+:*\w*|\(?\?\)?|\%\w+:*\w*|\$\w+:*\w*)\s*[\'\"]?)*\s?[\s\"\',]*where\s+((\w+:*\w*\s*!?=\s*[\'\":\\]*(\w+:*\w*|\(?\?\)?|\%\w+:*\w*|\$\w+:*\w*)\s*[\'\"\\]*\s*(and|or)?(\s*\w+:*\w*\s*!?=\s*[\'\":\\]*\s*(\w+:*\w*|\(?\?\)?|\%\w+:*\w*|\$\w+:*\w*)\s*[\'\":\\]*)*)|(\w+:*\w*\s+in\s*\(.+\))|(\w+:*\w*\s*is\s*null))'
    #regex = r'update\s\w+\sset\s*[\",\s\']*\s*\w+:*\w*\s*=\s*[\'\":\\]*\s*(\w+:*\w*|\(?\?\)?|\%\w+:*\w*|\$\w+:*\w*)\s*[\'\"\\]*(\s*[\+\-\*\/]\s*\d+)?(\s*,[\",\s\'\\]*\w+:*\w*\s*=\s*[\'\":\\]*\s*(\w+:*\w*|\(?\?\)?|\%\w+:*\w*|\$\w+:*\w*)\s*[\'\"]?)*\s?[\s\"\',]*where\s+(((and|or)?\s*\w+:*\w*\s*!?=[\s\'\":\\]*([\$\%]?\w+:*\w*|\(?\?\)?)[\s\'\":\\]*)|(\w+:*\w*\s+in\s*\(.+\))|(\w+:*\w*\s*is\s*(not)?\s*null))*'
    #regex = r'update\s\w+\sset\s?\w*:{0,2}\w*\s?=\s?(([\$\%]?\w*:{0,2}\w*)|(\(?\?\)?))\s?(\s?[\+\-\*\/]\s?\d+)?(\s?,\s?\w+:{0,2}\w*\s?=\s?(([\$\%]?\w*:{0,2}\w*)|(\(?\?\)?))\s?)*\swhere\s+(((and|or)?\s?\w+:{0,2}\w*\s?!?=\s?([\$\%]?\w*:{0,2}\w*|\(?\?\)?)\s?)|(\s?(and|or)?\s?\w+:{0,2}\w*\s+in\s?\(.+\))|(\s?(and|or)?\s?\w+:{0,2}\w*\s+is\s+(not)?\s?null))*'
    #regex = r'update\s\w+\sset\s(\s?,?\s?\w*:{0,2}\w*\s?=\s?(([\$\%]\w+)|(\w+)|(\w+:{1,2}\w+)|(:{1,2}\w+)|(\(?\?\)?))\s?(\s?[\+\-\*\/]\s?\d+)?)+\s?where\s+(((and|or)?\s?\w+:{0,2}\w*\s?!?=\s?(([\$\%]\w+)|(\w+)|(\w:{1,2}\w+)|(:{1,2}\w+)|(\(?\?\)?)\s?))|(\s?(and|or)?\s?\w+:{0,2}\w*\s+in\s?\(.+\))|(\s?(and|or)?\s?\w+:{0,2}\w*\s+is\s+(not)?\s?null))+'

    #I split the regular expression of update to simplify and make it faster.
    regex1 = r'update\s\w+\sset\s(\s?,?\s?\w*:{0,2}\w*\s?=\s?(([\$\%]\w+)|(\w+)|(\w+:{1,2}\w+)|(:{1,2}\w+)|(\(?\?\)?))\s?(\s?[\+\-\*\/]\s?\d+)?)+'
    regex2 = r'\s?where\s+(((and|or)?\s?\w+:{0,2}\w*\s?!?=\s?(([\$\%]\w+)|(\w+)|(\w:{1,2}\w+)|(:{1,2}\w+)|(\(?\?\)?)\s?))|(\s?(and|or)?\s?\w+:{0,2}\w*\s+in\s?\(.+\))|(\s?(and|or)?\s?\w+:{0,2}\w*\s+is\s+(not)?\s?null))+'
    match1 = re.search(regex1, line, flags=re.IGNORECASE)
    match2 = re.search(regex2, line, flags=re.IGNORECASE)
    if match1 and match2:
        return str(match1.group(0)) + str(match2.group(0))
    return ""

def processLine(inLine):
    line = inLine.strip('"')
    parsedStmt = SQLParse.SQLParse(line)
    if(parsedStmt.getStmtType()==SQLStmtType.SELECT):
        newline = cleanseSelectStmt(line)
        return newline
    if(parsedStmt.getStmtType()==SQLStmtType.CREATE):
        newline = cleanseCreateTable(parsedStmt.parsed)
        return newline
    if(parsedStmt.getStmtType()==SQLStmtType.INSERT):
        newline = cleanseCreateTable(parsedStmt.parsed)
        return newline
    if(parsedStmt.getStmtType()==SQLStmtType.UPDATE):
        #I removed all noise-generating characters to make regex simpler
        line = re.sub(r' +', r' ', line)
        line = re.sub(r'\'', r'', line)
        line = re.sub(r'\"', r'', line)
        line = re.sub(r'\t', r'', line)
        line = re.sub(r'\\', r'', line)
        newline = cleanseUpdateStatement(line)
        return newline
    if parsedStmt.getStmtType() == SQLStmtType.CREATE_INDEX:
        return line

i=1
for file in os.listdir(repoStoreRoot):
    if file.endswith(".sql"):
        print (str(i) + ":"+ str(file))
        i += 1
        if not os.path.exists(os.path.join(newRepoStoreRoot, file)):
            print ("...analyzing")
            with open(os.path.join(repoStoreRoot, file), "r", errors='ignore') as r:
                with open(os.path.join(newRepoStoreRoot, file), "w", errors='ignore') as w:
                    for line in r:
                        line = line.strip()
                        if len(line)> 1000:
                            line = line[:1000]
                        newline = processLine(line)
                        if not newline == "":
                            w.write(str(newline) + "\n")

