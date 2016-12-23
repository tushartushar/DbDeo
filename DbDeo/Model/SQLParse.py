import sqlparse
from sqlparse.tokens import DML, DDL, Keyword
from sqlparse.sql import IdentifierList, Identifier
from Model.SQLStmtType import SQLStmtType

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
        for token in self.parsed:
            if token.ttype is DML and token.value.upper() == 'SELECT':
                return SQLStmtType.SELECT
            if token.ttype is DDL and token.value.upper() == 'CREATE':
                return SQLStmtType.CREATE
            if token.ttype is DML and token.value.upper() == 'INSERT':
                return SQLStmtType.INSERT

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
                    yield identifier.get_name()
            elif isinstance(item, Identifier):
                yield item.get_name()
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
                                else:
                                    if not (value.value == ',' or value.value == ' '):
                                        values.append(value)
            if item.ttype is Keyword and item.value.upper() == 'VALUES':
                        values_seen = True
        return values