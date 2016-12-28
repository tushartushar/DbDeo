from unittest import TestCase

from Model import SQLParse
from Model.SQLStmtType import SQLStmtType
from Model.SelectStmt import SelectStmt
from Model.CreateStmt import CreateStmt
from Model.CreateIndexStmt import CreateIndexStmt

class ParseTests(TestCase):
    def test_checkStmtType_select(self):
        sqlStmt = "select empno id, ename employee, sal Salary, comm commission from emp where job = ''MANAGER'' and sal > 2000"
        parseObj = SQLParse.SQLParse(sqlStmt)
        self.assertEqual(parseObj.getStmtType(), SQLStmtType.SELECT)

    def test_checkStmtType_create(self):
        sqlStmt = "create table x_dump(clob_value clob, dump_date date default sysdate, dump_id number);elect empno id, ename employee, sal Salary, comm commission from emp where job = ''MANAGER'' and sal > 2000"
        parseObj = SQLParse.SQLParse(sqlStmt)
        self.assertEqual(parseObj.getStmtType(), SQLStmtType.CREATE)

    def test_checkStmtType_insert(self):
        sqlStmt = "INSERT INTO EMP VALUES(7934, 'MILLER', 'CLERK', 7782,TO_DATE('23-01-1982', 'DD-MM-YYYY'), 1300, NULL, 10);INSERT INTO DEPT VALUES (10, 'ACCOUNTING', 'NEW YORK'); "
        parseObj = SQLParse.SQLParse(sqlStmt)
        self.assertEqual(parseObj.getStmtType(), SQLStmtType.INSERT)

    def test_table_in_select(self):
        sqlStmt = "select empno id, ename employee, sal Salary, comm commission from emp where job = ''MANAGER'' and sal > 2000"
        parseObj = SQLParse.SQLParse(sqlStmt)
        selectStmt = SelectStmt(parseObj)
        selectStmt.populate()
        self.assertEqual(selectStmt.getReferencedTables(), ['emp'])

    def test_checkStmtType_createIndex(self):
        sqlStmt = "create index pIndex ON Persons (LastName, FirstName)"
        parseObj = SQLParse.SQLParse(sqlStmt)
        self.assertEqual(parseObj.getStmtType(), SQLStmtType.CREATE_INDEX)

    def test_where_in_select(self):
        sqlStmt = "select empno id, ename employee, sal Salary, comm commission from emp where job = ''MANAGER'' and sal > 2000"
        parseObj = SQLParse.SQLParse(sqlStmt)
        selectStmt = SelectStmt(parseObj)
        selectStmt.populate()
        self.assertEqual(selectStmt.isWherePresent(), True)

    def test_regex_in_where_in_select(self):
        sqlStmt = "SELECT * FROM Products WHERE account_id REGEXP '[[:<:]]12[[:>:]]';"
        parseObj = SQLParse.SQLParse(sqlStmt)
        selectStmt = SelectStmt(parseObj)
        selectStmt.populate()
        self.assertEqual(selectStmt.isRegexPresentInWhere(), True)

    def test_table_name_in_create(self):
        sqlStmt = "CREATE TABLE Comments (comment_id SERIAL PRIMARY KEY, parent_id BIGINT UNSIGNED, comment TEXT NOT NULL, FOREIGN KEY (parent_id) REFERENCES Comments(comment_id));"
        parseObj = SQLParse.SQLParse(sqlStmt)
        createStmt = CreateStmt(parseObj)
        createStmt.populate()
        self.assertEqual(createStmt.tableName, 'Comments')

    def test_table_column_count_in_create(self):
        sqlStmt = "CREATE TABLE Comments (comment_id SERIAL PRIMARY KEY, parent_id BIGINT UNSIGNED, comment TEXT NOT NULL, FOREIGN KEY (parent_id) REFERENCES Comments(comment_id));"
        parseObj = SQLParse.SQLParse(sqlStmt)
        createStmt = CreateStmt(parseObj)
        createStmt.populate()
        self.assertEqual(createStmt.getColumnCount(), 3)

    def test_table_name_in_createIndex(self):
        sqlStmt = "create index pIndex ON Persons (LastName, FirstName)"
        parseObj = SQLParse.SQLParse(sqlStmt)
        createIndexStmt = CreateIndexStmt(parseObj)
        createIndexStmt.populate()
        self.assertEqual(createIndexStmt.tableName, 'Persons')

    def test_columnList_in_createIndex(self):
        sqlStmt = "create index pIndex ON Persons (LastName, FirstName)"
        parseObj = SQLParse.SQLParse(sqlStmt)
        createIndexStmt = CreateIndexStmt(parseObj)
        createIndexStmt.populate()
        self.assertEqual(createIndexStmt.indexColumnList, ['LastName', 'FirstName'])

    def test_substitute_list_from(self):
        sqlStmt = "SELECT a.name, a.description, a.speed, b.name AS router FROM IssueAttributes a, router b WHERE a.rid=b.rid AND a.rid=$rid AND a.id=$iid[0]"
        parseObj = SQLParse.SQLParse(sqlStmt)
        selectStmt = SelectStmt(parseObj)
        selectStmt.populate()
        self.assertEqual(selectStmt.fromSubstituteList, {'a': 'IssueAttributes', 'b': 'router'})

    def test_from_table_list_in_select(self):
        sqlStmt = "SELECT a.name, a.description, a.speed, b.name AS router FROM IssueAttributes a, router b WHERE a.rid=b.rid AND a.rid=$rid AND a.id=$iid[0]"
        parseObj = SQLParse.SQLParse(sqlStmt)
        selectStmt = SelectStmt(parseObj)
        selectStmt.populate()
        self.assertEqual(selectStmt.fromTableList, ['IssueAttributes', 'router'])