# DbDeo - Database smell detector

## **Workflow**

It contains several components for downloading repos from github, collecting relevant metrics, and so on. Here is the how these tools can be used:

1. **Download repositories** - Use SQLRepoDownload to download repositories to analyze

2. **Extract SQL code** - Use SQLExtract and SQLCleanser to extract sql statements from the downloaded repositories 

3. **Collect basic metrics** - Use BasicDbMetrics to compute basic database metrics. Use ProgLangMetrics to compute number of files belonging to major programming language as well as total LOC, and total number of files in a set of repositories.

4. **Detect database smells** - Use DbDeo to detect database smells in the downloaded repos.

### SQLRepoDownload
This project downloads repositories provided via a csv file from GitHub and checks whether the downloaded repo has any SQL code. If the repo has SQL code, it retains the repo otherwise deletes it.

The entry file for the project is SQLRepoDownload/Main.py

### SQLExtract
SQL statement extraction happens in two stages. In the first stage, we analyze the whole repository (all the files), and extract sql statements (select, insert, and create), and put them in a sql file (one per each repo). In the second phase, we cleanse the extracted sql statements. In the first phase of sql statement extraction, we get a lot of noise because regex are not capable of covering all variations of sql statements. In this phase, we further cleanse the sql statements that we got from the first phase.

The entry file for the project is SQLExtract/Main.py

#### Using distribution
The compiled source has been put in ```SQLExtract_dist``` folder. You may directly execute the SQLExtract command on terminal (rather than installing dependencies and executing source code using python). The folder has executable files for Mac as well as for Windows operating system. Therefore, go to ```SQLExtract_dist\SQLExtract_win``` if you are working on Windows.

SQLExtract takes one parameter - the absolute path of the folder where you have put all the projects to analyze. For instance, if the folder
*/Users/Tushar/Workspace/all_projects* contains folders containing source code belonging to different projects such as *project1*, *project2*, and so on, then specify the following command:
```
$ ./SQLExtract /Users/Tushar/Workspace/all_projects/
```

### BasicDbMetrics
- This project computes basic database metrics such as number of select, insert, and create table statements per repository. The entry file for the project is Main.py
- Use ProgLangMetrics.py to compute number of files belonging to major programming language as well as total LOC, and total number of files in a set of repositories.

### DbDeo
This project analyzes database code and detect database smells. Currently, it supports detection of following database smells:
- Compound Attribute
- Adjacency List
- God Table
- Values in Column Definition
- Metadata as Data
- Multicolumn Attribute
- Clone Tables
- Duplicate Column Names
- Index Shotgun
- Obsolete Column Types

The entry file for the project is DbDeo/Main.py

You may aggregate the results by using Aggregator/Aggregator.py