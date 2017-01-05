class UpdateStmt(object):
    def __init__(self, parsedStmt):
        self.parsedStmt = parsedStmt
        self.setExpn = ""

    def populate(self):
        self.setExpn = self.parsedStmt.getSetExpn()
        #This restriction is being put to eliminate extra information because sql statement extraction
        #extracts more than sql statements sometimes
        if len(self.setExpn) > 80 or (not '=' in self.setExpn):
            self.setExpn =""

    def isContainsCommaInSet(self):
        if ',' in self.setExpn:
            return True
        return False