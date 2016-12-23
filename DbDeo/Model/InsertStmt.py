class InsertStmt(object):
    def __init__(self, parsedStmt):
        self.parsedStmt = parsedStmt

    def populate(self):
        self.valueList = self.parsedStmt.getInsertedValues()

    def isContainsCompoundAttribute(self):
        for token in self.valueList:
            if ',' in token.value:
                return True
        return False