import Model.DataTypeConstants as DataTypes

class TableColumn(object):
    def __init__(self, parsedColumn):
        self.parsedColumn = parsedColumn
        self.columnType = ""
        self.isPrimaryKey = False
        self.isForeignKey = False
        self.isNotNull = False
        self.isReferences = False
        self.referencedTable = ""
        self.isConstraint = False
        self.areValuesConstrained = False
        self.referencedColumnList = []
        self.populate()
        self.shortColumnType = "" #This field captures the precise data type removing extra information present in columnType
        self.extractColumnShortType()

    def populate(self):
        name_seen = False
        ref_seen = False
        ref_table_seen = False
        for item in self.parsedColumn:
            if item.is_whitespace or item.value == '(' or item.value == ')' or item.value.upper() == 'KEY':
                continue
            if self.isPrimaryKey and self.isConstraint:
                self.referencedColumnList.append(item.value)
            if item.value.upper() == 'PRIMARY':
                self.isPrimaryKey = True
                if not name_seen:
                    self.isConstraint = True
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
                self.referencedColumnList.append(item.value)
            elif item.value.upper() == 'NOT NULL':
                self.isNotNull = True
            elif item.value.upper() == 'CHECK' or item.value.upper() == 'ENUM':
                self.areValuesConstrained = True
            elif not name_seen:
                self.columnName = item.value
                name_seen = True
            elif name_seen:
                if not self.columnType == "":
                    self.columnType += " "
                self.columnType += item.value

    def extractColumnShortType(self):
        if DataTypes.ARRAY in self.columnType.upper():
            self.shortColumnType = DataTypes.ARRAY
        elif DataTypes.BIGINT in self.columnType.upper():
            self.shortColumnType = DataTypes.BIGINT
        elif DataTypes.VARBINARY in self.columnType.upper():
            self.shortColumnType = DataTypes.VARBINARY
        elif DataTypes.BINARY in self.columnType.upper():
            self.shortColumnType = DataTypes.BINARY
        elif DataTypes.BIT in self.columnType.upper():
            self.shortColumnType = DataTypes.BIT
        elif DataTypes.BOOLEAN in self.columnType.upper():
            self.shortColumnType = DataTypes.BOOLEAN
        elif DataTypes.CHARACTER in self.columnType.upper():
            self.shortColumnType = DataTypes.CHARACTER
        elif DataTypes.NCHAR in self.columnType.upper():
            self.shortColumnType = DataTypes.NCHAR
        elif DataTypes.NVARCHAR in self.columnType.upper():
            self.shortColumnType = DataTypes.NVARCHAR
        elif DataTypes.VARCHAR in self.columnType.upper():
            self.shortColumnType = DataTypes.VARCHAR
        elif DataTypes.CHAR in self.columnType.upper():
            self.shortColumnType = DataTypes.CHAR
        elif DataTypes.CURSOR in self.columnType.upper():
            self.shortColumnType = DataTypes.CURSOR
        elif DataTypes.DATETIMEOFFSET in self.columnType.upper():
            self.shortColumnType = DataTypes.DATETIMEOFFSET
        elif DataTypes.DATETIME2 in self.columnType.upper():
            self.shortColumnType = DataTypes.DATETIME2
        elif DataTypes.DATETIME in self.columnType.upper():
            self.shortColumnType = DataTypes.DATETIME
        elif DataTypes.DATE in self.columnType.upper():
            self.shortColumnType = DataTypes.DATE
        elif DataTypes.DECIMAL in self.columnType.upper():
            self.shortColumnType = DataTypes.DECIMAL
        elif DataTypes.DOUBLE_PRECISION in self.columnType.upper():
            self.shortColumnType = DataTypes.DOUBLE_PRECISION
        elif DataTypes.FLOAT in self.columnType.upper():
            self.shortColumnType = DataTypes.FLOAT
        elif DataTypes.HIERARCHYID in self.columnType.upper():
            self.shortColumnType = DataTypes.HIERARCHYID
        elif DataTypes.IMAGE in self.columnType.upper():
            self.shortColumnType = DataTypes.IMAGE
        elif DataTypes.INTEGER in self.columnType.upper():
            self.shortColumnType = DataTypes.INTEGER
        elif DataTypes.SMALLINT in self.columnType.upper():
            self.shortColumnType = DataTypes.SMALLINT
        elif DataTypes.TINYINT in self.columnType.upper():
            self.shortColumnType = DataTypes.TINYINT
        elif DataTypes.INT in self.columnType.upper():
            self.shortColumnType = DataTypes.INT
        elif DataTypes.INTERVAL in self.columnType.upper():
            self.shortColumnType = DataTypes.INTERVAL
        elif DataTypes.SMALLMONEY in self.columnType.upper():
            self.shortColumnType = DataTypes.SMALLMONEY
        elif DataTypes.MONEY in self.columnType.upper():
            self.shortColumnType = DataTypes.MONEY
        elif DataTypes.MULTISET in self.columnType.upper():
            self.shortColumnType = DataTypes.MULTISET
        elif DataTypes.NTEXT in self.columnType.upper():
            self.shortColumnType = DataTypes.NTEXT
        elif DataTypes.NUMERIC in self.columnType.upper():
            self.shortColumnType = DataTypes.NUMERIC
        elif DataTypes.NUMBER in self.columnType.upper():
            self.shortColumnType = DataTypes.NUMBER
        elif DataTypes.REAL in self.columnType.upper():
            self.shortColumnType = DataTypes.REAL
        elif DataTypes.SMALLDATETIME in self.columnType.upper():
            self.shortColumnType = DataTypes.SMALLDATETIME
        elif DataTypes.SPATIAL_TYPES in self.columnType.upper():
            self.shortColumnType = DataTypes.SPATIAL_TYPES
        elif DataTypes.SQL_VARIANT in self.columnType.upper():
            self.shortColumnType = DataTypes.SQL_VARIANT
        elif DataTypes.TABLE in self.columnType.upper():
            self.shortColumnType = DataTypes.TABLE
        elif DataTypes.TEXT in self.columnType.upper():
            self.shortColumnType =DataTypes.TEXT
        elif DataTypes.TIMESTAMP in self.columnType.upper():
            self.shortColumnType = DataTypes.TIMESTAMP
        elif DataTypes.TIME in self.columnType.upper():
            self.shortColumnType = DataTypes.TIME
        elif DataTypes.UNIQUEIDENTIFIER in self.columnType.upper():
            self.shortColumnType = DataTypes.UNIQUEIDENTIFIER
        elif DataTypes.XML in self.columnType.upper():
            self.shortColumnType = DataTypes.XML
        else:
            self.shortColumnType = self.columnType.upper()

