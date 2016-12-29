class CreateIndexStmt(object):
    def __init__(self, parsedStmt):
        self.parsedStmt = parsedStmt
        self.tableName = ""
        self.indexColumnList = []

    def populate(self):
        self.tableName = self.parsedStmt.getTableNameInCreateIndex()
        self.indexColumnList = self.parsedStmt.getIndexColumnList()

