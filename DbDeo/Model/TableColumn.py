class TableColumn(object):
    def __init__(self, parsedColumn):
        self.parsedColumn = parsedColumn
        self.columnType = ""
        self.isPrimaryKey = False
        self.isForeignKey = False
        self.isNotNull = False
        self.isReferences = False
        self.referencedTable = ""
        self.referencedColumn = ""
        self.isConstraint = False
        self.populate()

    def populate(self):
        name_seen = False
        ref_seen = False
        ref_table_seen = False
        for item in self.parsedColumn:
            if item.value == ' ' or item.value == '(' or item.value == ')' or item.value.upper() == 'KEY':
                continue
            if item.value.upper() == 'PRIMARY':
                self.isPrimaryKey = True
            elif item.value.upper() == 'FOREIGN':
                self.isForeignKey = True
                if not name_seen:
                    self.isConstraint = True
            elif item.value.upper() == 'REFERENCES':
                self.isReferences = True
                ref_seen = True
            elif ref_seen and not ref_table_seen:
                self.referencedTable = item.value
                ref_table_seen = True
            elif ref_table_seen:
                if not self.referencedColumn == "":
                    self.referencedColumn += " "
                self.referencedColumn = item.value
            elif item.value.upper() == 'NOT NULL':
                self.isNotNull = True
            elif not name_seen:
                self.columnName = item.value
                name_seen = True
            elif name_seen:
                if not self.columnType == "":
                    self.columnType += " "
                self.columnType += item.value