class CreateStmt(object):
    def __init__(self, parsedStmt):
        self.parsedStmt = parsedStmt

    def populate(self):
        self.tableName = self.parsedStmt.getTableName()
        self.columnList = self.parsedStmt.getColumnList()

    def getColumnCount(self):
        count = 0
        for col in self.columnList:
            if not col.isConstraint:
                count += 1
        return count
