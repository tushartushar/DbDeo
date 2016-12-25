class InsertStmt(object):
    def __init__(self, parsedStmt):
        self.parsedStmt = parsedStmt

    def populate(self):
        self.valueList = self.parsedStmt.getInsertedValues()

    def isContainsCompoundAttribute(self):
        for token in self.valueList:
            if ',' in token.value:
                #This check is required to eliminate false positives where a method is used such as TO_DATE('23-01-1982', 'DD-MM-YYYY')
                if not ('(' in token.value or ')' in token.value):
                    return True
        return False