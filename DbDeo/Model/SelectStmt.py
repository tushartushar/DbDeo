import re

class SelectStmt(object):
    def __init__(self, parsedStmt):
        self.parsedStmt = parsedStmt

    def populate(self):
        self.tables = self.parsedStmt.populateReferencedTables(self.parsedStmt.parsed)
        self.whereConditionList = self.parsedStmt.populateWhereConditions()

    def getReferencedTables(self):
        return self.tables

    def isWherePresent(self):
        if(len(self.whereConditionList)>0):
            return True
        else:
            return False

    def isRegexPresentInWhere(self):
        for whereCondition in self.whereConditionList:
            if re.search('regexp', whereCondition, re.IGNORECASE):
                return True
        return False

