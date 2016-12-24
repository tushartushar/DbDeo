class UpdateStmt(object):
    def __init__(self, parsedStmt):
        self.parsedStmt = parsedStmt

    def populate(self):
        self.setExpn = self.parsedStmt.getSetExpn()

    def isContainsCommaInSet(self):
        for token in self.setExpn:
            if ',' in token.value:
                return True
        return False