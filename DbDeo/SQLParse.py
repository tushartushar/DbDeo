import sqlparse
from sqlparse.tokens import Keyword, DML, DDL
from SQLStmtType import SQLStmtType

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