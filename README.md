# DbDeo
Database smell detector

It contains several components for downloading repos from github, collecting relevant metrics, and so on. A brief description of these components are given below.

##SQLRepoDownload
This project downloads repositories provided via a csv file from GitHub and checks whether the downloaded repo has any SQL code. If the repo has SQL code, it retains the repo otherwise deletes it.

The entry file for the project is Main.py

##SQLExtract
This project analyzes repositories, extract sql statements (select, insert, and create), and put them in a sql file (one per each repo).

The entry file for the project is Main.py

##BasicDbMetrics
This project computes basic database metrics such as number of select, insert, and create table statements per repository.

The entry file for the project is Main.py