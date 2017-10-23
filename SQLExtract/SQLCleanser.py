import re
from Model import SQLParse
from Model.SQLStmtType import SQLStmtType

def processLine(inLine):
    line = inLine.strip('"')
    #print(line)
    try:
        parsedStmt = SQLParse.SQLParse(line)
    except:
        return ""
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
        newline = cleanseIndexStmt(parsedStmt.parsed)
        return newline

def cleanseCreateTable(parsedStmt):
    count = 0
    newline = ""
    bracket_seen = False
    name_seen = False
    trip_next = False
    for token in parsedStmt.flatten():
        token_value = token.value.upper()
        if (not name_seen) and (not token_value in [' ', 'CREATE', 'TABLE', 'IF', 'NOT', 'EXISTS', 'INSERT', 'INTO', 'VALUES']):
            name_seen = True
        elif token.value == '(':
            count += 1
            bracket_seen = True
            trip_next = False
        elif token.value == ')':
            count -= 1
            if count <= 0:
                newline += token.value
                if bracket_seen:
                    return newline
                else:
                    return ""
        elif name_seen and (not bracket_seen):
            if token.value.upper() == 'VALUES':
                trip_next = False
            else:
                if trip_next:
                    return ""
                if token.value == ' ': #there are useless words... probably not a correct create statement
                    trip_next = True

        newline += token.value

    return ""


def cleanseSelectStmt(line):
    regex = r'select\s+(\%?\w+(\(\w+\))?|(\w+\()?\*\)?)(\s?,\s?\%?\w+(\(\w+|\*\))?)*\s+from\s+(.+\s?)(where\s+(((and|or)?\s?\w+:{0,2}\w*\s?!?=\s?(([\$\%]\w+)|(\w+)|(\w:{1,2}\w+)|(:{1,2}\w+)|(\(?\?\)?)\s?)))*?)?\s?(order\sby.+\n)?\s?(group\sby\s\w+)?'
    match = re.search(regex, line, flags=re.IGNORECASE)
    if match:
        return str(match.group(0))
    return ""


def cleanseUpdateStatement(line):
    #I split the regular expression of update to simplify and make it faster.
    regex1 = r'update\s\w+\sset\s(\s?,?\s?\w*:{0,2}\w*\s?=\s?(([\$\%]\w+)|(\w+)|(\w+:{1,2}\w+)|(:{1,2}\w+)|(\(?\?\)?))\s?(\s?[\+\-\*\/]\s?\d+)?)+'
    regex2 = r'\s?where\s+(((and|or)?\s?\w+:{0,2}\w*\s?!?=\s?(([\$\%]\w+)|(\w+)|(\w:{1,2}\w+)|(:{1,2}\w+)|(\(?\?\)?)\s?))|(\s?(and|or)?\s?\w+:{0,2}\w*\s+in\s?\(.+\))|(\s?(and|or)?\s?\w+:{0,2}\w*\s+is\s+(not)?\s?null))+'
    match1 = re.search(regex1, line, flags=re.IGNORECASE)
    match2 = re.search(regex2, line, flags=re.IGNORECASE)
    if match1 and match2:
        return str(match1.group(0)) + str(match2.group(0))
    return ""


def cleanseIndexStmt(parsedStmt):
    newline = ""
    on_seen = False
    for token in parsedStmt.flatten():
        if token.value.upper() == 'ON':
            on_seen = True
        elif on_seen and token.is_keyword:
            return newline
        newline += token.value
    return newline
