import sqlparse
from sqlparse.tokens import DML, DDL, Keyword
from sqlparse.sql import IdentifierList, Identifier
from Model.SQLStmtType import SQLStmtType
from Model.TableColumn import TableColumn
import Model.DataTypeConstants as DataTypes

class SQLParse(object):
    def __init__(self, stmt):
        self.stmt = stmt
        self.parsed = sqlparse.parse(stmt)[0]
        self.sqlStmtType = self.knowStmtType()
        #self.printAll(self.parsed)

    def printAll(self, parsed):
        for token in parsed.tokens:
            print("Token: " + str(token) + " \nType: " + str(token.ttype) + " \nStmt type: " + str(token.value.upper))

    def knowStmtType(self):
        create_seen = False
        for token in self.parsed:
            if token.ttype is DML and token.value.upper() == 'SELECT':
                return SQLStmtType.SELECT
            if token.ttype is DDL and token.value.upper() == 'CREATE':
                create_seen = True
                continue
            if token.ttype is Keyword and token.value.upper() == 'TABLE' and create_seen:
                return SQLStmtType.CREATE
            if token.ttype is Keyword and token.value.upper() == 'INDEX' and create_seen:
                return SQLStmtType.CREATE_INDEX
            if token.ttype is DML and token.value.upper() == 'INSERT':
                return SQLStmtType.INSERT
            if token.ttype is DML and token.value.upper() == 'UPDATE':
                return SQLStmtType.UPDATE
        return SQLStmtType.DEFAULT

    def getStmtType(self):
        return self.sqlStmtType

    def populateWhereConditions(self):
        whereExpn = self.traverseForWhere()
        whereExpnList = self.splitExpn(whereExpn)
        return whereExpnList

    def populateReferencedTables(self, parsedStmt):
        stream = self.extractFromPart(parsedStmt)
        return list(self.extractTableIdentifiers(stream))

    def extractFromPart(self, parsed):
        from_seen = False
        for item in parsed.tokens:
            if from_seen:
                if self.isSubSelect(item):
                    for x in self.extractFromPart(item):
                        yield x
                elif item.ttype is Keyword:
                    raise StopIteration
                else:
                    yield item
            elif item.ttype is Keyword and item.value.upper() == 'FROM':
                from_seen = True

    def extractTableIdentifiers(self, token_stream):
        for item in token_stream:
            if isinstance(item, IdentifierList):
                for identifier in item.get_identifiers():
                    try:
                        yield identifier.get_name()
                    except:
                        pass
            elif isinstance(item, Identifier):
                try:
                    yield item.get_name()
                except:
                    pass
            # It's a bug to check for Keyword here, but in the example
            # above some tables names are identified as keywords...
            elif item.ttype is Keyword:
                yield item.value

    def isSubSelect(self, parsed):
        if not parsed.is_group:
            return False
        for item in parsed.tokens:
            if item.ttype is DML and item.value.upper() == 'SELECT':
                return True
        return False

    def traverseForWhere(self):
        where_seen = False
        whereExpn = []
        for item in self.parsed.tokens:
            if item.is_group:
                for token in item.tokens:
                    if where_seen:
                        if token.ttype is Keyword and not (token.value.upper() == 'AND' or token.value.upper() == 'OR'):
                            return whereExpn
                        else:
                            whereExpn.append(token)
                    elif token.ttype is Keyword and token.value.upper() == 'WHERE':
                        where_seen = True
        return whereExpn

    def splitExpn(self, whereExpn):
        expnList = []
        curExpn = ""
        for item in whereExpn:
            if item.ttype is Keyword:
                if not curExpn == "":
                    expnList.append(curExpn.strip())
                    curExpn = ""
            else:
                curExpn += item.value
        if not curExpn == "":
            expnList.append(curExpn.strip())
        return expnList

    def extractAttributesInWhere(self):
        whereExpn = self.traverseForWhere()
        resultList = []
        curResult = ""
        for item in whereExpn:
            for token in item.flatten():
                if token.value == ' ':
                    continue
                if token.value == ';' or token.value == '{':
                    if not curResult == "":
                        resultList.append(curResult)
                    return resultList
                if token.value.upper() in ['==', '=', '>', '>=', '<', '<=', '<>', 'LIKE', 'BETWEEN', 'IN'] or token.is_keyword:
                    if not curResult =="":
                        resultList.append(curResult)
                        curResult =""
                    continue
                else:
                    curResult += token.value
        if not curResult == "":
            resultList.append(curResult)
        return resultList

    def getInsertedValues(self):
        values_seen = False
        values = []
        for item in self.parsed.tokens:
            if item.is_group:
                for token in item.tokens:
                    if values_seen:
                        if token.is_group:
                            for value in token.tokens:
                                if value.ttype is Keyword and not (value.value.upper() == 'DEFAULT'):
                                    return values
                                if value.value == ';' or value.value == '{':
                                    return values
                                else:
                                    if not (value.value == ',' or value.value == ' '):
                                        values.append(value)
            if item.ttype is Keyword and item.value.upper() == 'VALUES':
                        values_seen = True
        return values

    def getSetExpn(self):
        set_seen = False
        values = ""
        for item in self.parsed.tokens:
            if set_seen:
                if item.is_group:
                    for value in item.tokens:
                        if value.ttype is Keyword:
                            return values
                        else:
                            if value.is_group:
                                for node in value.tokens:
                                    if node.ttype is Keyword:
                                        return values
                                    else:
                                        values += node.value
                            else:
                                values += value.value
                else:
                    values += item.value
            if item.ttype is Keyword and item.value.upper() == 'SET':
                set_seen = True
        return values

    def getTableName(self):
        create_seen = False
        table_seen = False
        for token in self.parsed.tokens:
            if create_seen:
                if table_seen:
                    if not token.value == ' ':
                        if token.is_group:
                            for item in token.tokens:
                                if not item.is_keyword:
                                    return item.value
                        else:
                            if not token.is_keyword:
                                return token.value
                else:
                    if token.ttype is Keyword and token.value.upper() == 'TABLE':
                        table_seen = True
            else:
                b1 = token.is_keyword
                b2 = token.value.upper() == 'CREATE'
                if b1 and b2:
                    create_seen = True
        return ""

    def getTableNameInCreateIndex(self):
        on_seen = False
        for token in self.parsed.tokens:
            if on_seen:
                if not token.value == ' ':
                    if token.is_group:
                        for item in token.tokens:
                            return item.value
                    else:
                        return token.value
            else:
                b1 = token.is_keyword
                b2 = token.value.upper() == 'ON'
                if b1 and b2:
                    on_seen = True
        return ""

    def getColumnDefinitionExpn(self):
        result = []
        create_seen = False
        table_seen = False
        name_seen = False
        for token in self.parsed.tokens:
            if create_seen:
                if table_seen:
                    if not token.value == ' ':
                        if token.is_group:
                            for item in token.tokens:
                                if item.is_group:
                                    for node in item.tokens:
                                        if not name_seen:
                                            name_seen = True
                                            continue
                                        if name_seen:
                                            result.append(node)
                                else:
                                    if not name_seen:
                                        name_seen = True
                                        continue
                                    if name_seen:
                                        result.append(item)
                        else:
                            if not name_seen:
                                name_seen = True
                                continue
                            if name_seen:
                                result.append(token)
                else:
                    if token.ttype is Keyword and token.value.upper() == 'TABLE':
                        table_seen = True
            else:
                b1 = token.is_keyword
                b2 = token.value.upper() == 'CREATE'
                if b1 and b2:
                    create_seen = True
        return result

    def getColumnList(self):
        expn = self.getColumnDefinitionExpn()
        columns = self.extract_definitions(expn)
        columnObjs = self.createColumnObjects(columns)
        return columnObjs

    def extract_definitions(self, token_list):
        definitions = []
        curDef = []
        paranthesis_depth = 0
        for token in token_list:
            if token.value == '(':
                paranthesis_depth += 1
                continue
            if token.value == ')':
                paranthesis_depth -= 1
                continue
            if token.is_group:
                for node in token.tokens:
                    if node.value == ',':
                        if paranthesis_depth <= 1:
                            if not curDef == []:
                                definitions.append(curDef)
                                curDef = []
                        else:
                            curDef.append(node)
                    else:
                        curDef.append(node)
            elif token.value == ',':
                if paranthesis_depth <= 1:
                    if not curDef == []:
                        definitions.append(curDef)
                        curDef = []
                else:
                    curDef.append(token)
            else:
                curDef.append(token)
        if not curDef == []:
            definitions.append(curDef)
        return definitions

    def createColumnObjects(self, columns):
        columnObjs = []
        for column in columns:
            tableColumn = TableColumn(column)
            #This restriction is being put to eliminate extra information because sql statement extraction
            #extracts more than sql statements sometimes
            if tableColumn.shortColumnType == DataTypes.UNKNOWN:
                if tableColumn.isConstraint or tableColumn.isPrimaryKey or tableColumn.isForeignKey:
                    columnObjs.append(tableColumn)
            else:
                columnObjs.append(tableColumn)
        return columnObjs

    def getIndexColumnList(self):
        on_seen = False
        name_seen = False
        columnList = []
        for token in self.parsed.tokens:
            if on_seen:
                if not token.value == ' ':
                    if token.is_group:
                        for item in token.flatten():
                            if not name_seen:
                                name_seen = True
                                continue
                            if not (item.value == ' ' or item.value == '(' or item.value == ')' or item.value == ','):
                                columnList.append(item.value)
                            if item.value == ';':
                                return columnList
                    else:
                        name_seen = True
            else:
                b1 = token.is_keyword
                b2 = token.value.upper() == 'ON'
                if b1 and b2:
                    on_seen = True
        return columnList

    def populateFromSubstituteList(self):
        from_seen = False
        resultList = dict()
        curTable = ""
        curSub = ""
        curTable_seen = False
        for token in self.parsed.tokens:
            for item in token.flatten():
                if (item.value == ' ' or item.value == '(' or item.value == ')'):
                    continue
                if from_seen:
                    if item.is_keyword:
                        if (not curTable == "") and (not curSub == ""):
                            resultList[curSub] = curTable
                            curTable = ""
                            curSub = ""
                            curTable_seen = False
                        return resultList
                    if item.value == ',':
                        if (not curTable == "") and (not curSub == ""):
                            resultList[curSub] = curTable
                            curTable = ""
                            curSub = ""
                            curTable_seen = False
                    elif curTable_seen:
                        curSub = item.value
                    else:
                        curTable = item.value
                        curTable_seen = True
                else:
                    b1 = item.is_keyword
                    b2 = item.value.upper() == 'FROM'
                    if b1 and b2:
                        from_seen = True
        return resultList

    def populateFromTableList(self):
        from_seen = False
        resultList = []
        curTable_seen = False
        for token in self.parsed.tokens:
            for item in token.flatten():
                if (item.value == ' ' or item.value == '(' or item.value == ')'):
                    continue
                if from_seen:
                    if item.is_keyword:
                        return resultList
                    if item.value == ',':
                        curTable_seen = False
                    elif curTable_seen:
                        continue
                    else:
                        resultList.append(item.value)
                        curTable_seen = True
                else:
                    b1 = item.is_keyword
                    b2 = item.value.upper() == 'FROM'
                    if b1 and b2:
                        from_seen = True
        return resultList
