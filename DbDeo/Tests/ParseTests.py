from unittest import TestCase
from SQLStmtType import SQLStmtType
import SQLParse


class ParseTests(TestCase):
    def test_checkStmtType_select(self):
        sqlStmt = "select empno id, ename employee, sal Salary, comm commission from emp where job = ''MANAGER'' and sal > 2000', dbms_sql.native );"

        parseObj = SQLParse.SQLParse(sqlStmt)

        self.assertEqual(parseObj.getStmtType(), SQLStmtType.SELECT)

    def test_checkStmtType_create(self):
        sqlStmt = "create table x_dump(clob_value clob, dump_date date default sysdate, dump_id number);elect empno id, ename employee, sal Salary, comm commission from emp where job = ''MANAGER'' and sal > 2000', dbms_sql.native );"

        parseObj = SQLParse.SQLParse(sqlStmt)

        self.assertEqual(parseObj.getStmtType(), SQLStmtType.CREATE)

    def test_checkStmtType_insert(self):
        sqlStmt = "INSERT INTO EMP VALUES(7934, 'MILLER', 'CLERK', 7782,TO_DATE('23-01-1982', 'DD-MM-YYYY'), 1300, NULL, 10);INSERT INTO DEPT VALUES (10, 'ACCOUNTING', 'NEW YORK'); "
        parseObj = SQLParse.SQLParse(sqlStmt)

        self.assertEqual(parseObj.getStmtType(), SQLStmtType.INSERT)