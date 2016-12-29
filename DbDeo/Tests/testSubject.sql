select * from dba_datapump_jobs;
select ename from emp order by ename;
select empno id, ename employee, sal Salary, comm commission from emp where job = ''MANAGER'' and sal > 2000', dbms_sql.native );
"select * from sample where x > 3"

create table x_dump2000(clob_value clob, dump_date date default sysdate, dump_id number);
create table x_dump2001(clob_value blob, dump_date date default sysdate, dump_id number, clob_value2 clob, dump_date2 date default sysdate, dump_id2 number, clob_value3 clob, dump_date3 date default sysdate, dump_id3 number, clob_value4 clob, dump_date4 date default sysdate, dump_id4 number);
INSERT INTO EMP VALUES(7934, 'MILLER', 'CLERK', 7782,TO_DATE('23-01-1982', 'DD-MM-YYYY'), 1300, NULL, 10);
INSERT INTO DEPT VALUES (10, 'ACCOUNTING', 'NEW YORK');

SELECT * FROM Products WHERE account_id REGEXP '[[:<:]]12[[:>:]]';
INSERT INTO Products (product_id, product_name, account_id) VALUES (DEFAULT, 'Visual TurboBuilder', '12,34,banana');
UPDATE Products SET account_id = account_id || ',' || 56 WHERE product_id = 123;
CREATE TABLE Comments (comment_id SERIAL PRIMARY KEY, parent_id BIGINT UNSIGNED, comment TEXT NOT NULL, FOREIGN KEY (parent_id) REFERENCES Comments(comment_id));
CREATE TABLE Bugs (comment_id SERIAL PRIMARY KEY, clob_value clob, status VARCHAR(20) CHECK (status IN ('NEW', 'IN PROGRESS', 'FIXED')) );

CREATE TABLE IssueAttributes (  issue_id    BIGINT UNSIGNED NOT NULL,  attr_name   VARCHAR(100) NOT NULL,  attr_value  VARCHAR(100),  PRIMARY KEY (issue_id, attr_name), FOREIGN KEY (issue_id) REFERENCES Issues(issue_id));
CREATE TABLE Bugs (        bug_id      SERIAL PRIMARY KEY,        description VARCHAR(1000),        tag1        VARCHAR(20),        tag2        VARCHAR(20), tag3        VARCHAR(20));
CREATE TABLE Customers (  customer_id    BIGINT UNSIGNED NOT NULL,  name   VARCHAR(100) NOT NULL,  surname  TEXT,  preferences NTEXT, PRIMARY KEY (customer_id), FOREIGN KEY (issue_id) REFERENCES Issues(issue_id));
