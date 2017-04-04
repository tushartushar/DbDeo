class CreateStmt(object):
    def __init__(self, parsedStmt):
        self.parsedStmt = parsedStmt
        self.tableName = ""
        self.columnList = []

    def populate(self):
        self.tableName = self.parsedStmt.getTableName()
        self.columnList = self.parsedStmt.getColumnList()

    def getColumnCount(self):
        count = 0
        for col in self.columnList:
            if not col.isConstraint:
                count += 1
        return count

    def getKeyList(self):
        keyList = []
        for column in self.columnList:
            if column.isPrimaryKey:
                if column.isConstraint:
                    for refCol in column.referencedColumnList:
                        if not (refCol == ' ' or refCol == ',' or refCol == ';'):
                            keyList.append([self.tableName, refCol])
                else:
                    keyList.append([self.tableName, column.columnName])
            elif column.isForeignKey:
                if column.isConstraint:
                    for refCol in column.referencedColumnList:
                        if not (refCol == ' ' or refCol == ',' or refCol == ';'):
                            keyList.append([column.referencedTable, refCol])
        return keyList

    def getForeignKeyList(self):
        keyList = []
        for column in self.columnList:
            if column.isForeignKey:
                if column.isConstraint:
                    for refCol in column.referencedColumnList:
                        if not (refCol == ' ' or refCol == ',' or refCol == ';'):
                            keyList.append([column.referencedTable, refCol])
        return keyList