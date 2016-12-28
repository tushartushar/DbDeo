import re

class SelectStmt(object):
    def __init__(self, parsedStmt):
        self.fromSubstituteList = None
        self.parsedStmt = parsedStmt

    def populate(self):
        self.tables = self.parsedStmt.populateReferencedTables(self.parsedStmt.parsed)
        self.whereConditionList = self.parsedStmt.populateWhereConditions()
        self.fromTableList = self.parsedStmt.populateFromTableList()
        attributesInWhereList = self.parsedStmt.extractAttributesInWhere()
        self.fromSubstituteList = self.parsedStmt.populateFromSubstituteList()
        self.attributesInWhereList = self.setAttributesInWhereList(attributesInWhereList) #list contains tupes ['table', 'attributte']

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

    def setAttributesInWhereList(self, attributesInWhereList):
        list = []
        for attr in attributesInWhereList:
            if '.' in attr:
                m = re.search('(\w+)\.(\w+)', attr)
                if m:
                    if not self.fromSubstituteList[m.group(1)] == None:
                        list.append([self.fromSubstituteList[m.group(1)], m.group(2)])
                    else:
                        list.append([m.group(1), m.group(2)])
            else:
                for table in self.fromTableList: #add all tables to avoid false positives
                    list.append([table, attr])
        return list


