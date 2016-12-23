select * from dba_datapump_jobs;
select ename from emp order by ename;
select empno id, ename employee, sal Salary, comm commission from emp where job = ''MANAGER'' and sal > 2000', dbms_sql.native );
"select * from sample where x > 3"

create table x_dump(clob_value clob, dump_date date default sysdate, dump_id number);
 
INSERT INTO EMP VALUES(7934, 'MILLER', 'CLERK', 7782,TO_DATE('23-01-1982', 'DD-MM-YYYY'), 1300, NULL, 10);
INSERT INTO DEPT VALUES (10, 'ACCOUNTING', 'NEW YORK');
 
SELECT * FROM Products WHERE account_id REGEXP '[[:<:]]12[[:>:]]';
INSERT INTO Products (product_id, product_name, account_id) VALUES (DEFAULT, 'Visual TurboBuilder', '12,34,banana');