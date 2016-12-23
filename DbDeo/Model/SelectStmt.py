

class SelectStmt(object):
    def __init__(self, parsedStmt):
        self.parsedStmt = parsedStmt

    def populate(self):
        self.tables = self.parsedStmt.populateReferencedTables(self.parsedStmt.parsed)

    def getReferencedTables(self):
        return self.tables

