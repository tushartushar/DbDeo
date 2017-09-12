import os
import FileUtils
import re


def logit(result):
    print("Match found: " + result.group(0))
    #Utils.FileUtils.writeFile(logFile, "Match found: " + result.group(0))

def check_file_for_orm(file):
    contents = FileUtils.readFileContents(file)

    result = re.search(r"#include\s?<sqlite3\.h>", contents)
    if(result!=None):
        logit(result)
        return "c++litesql"

    result = re.search(r"#include\s?<odb/database\.hxx>", contents)
    if(result!=None):
        logit(result)
        return "C++odb"

    result = re.search(r"#include\s?<QxOrm\.h>", contents)
    if(result!=None):
        logit(result)
        return "C++QxOrm"

    result = re.search(r"import\sorg\.javalite\.activejdbc", contents)
    if(result!=None):
        logit(result)
        return "JavaActiveJdbc"

    result = re.search(r"import\sorg\.apache\.Cayenne", contents)
    if(result!=None):
        logit(result)
        return "JavaCayenne"

    result = re.search(r"name\s?=\s?\"eclipselink\.jdbc\.driver\"", contents)
    if(result!=None):
        logit(result)
        return "JavaEclipseLink"

    result = re.search(r"import\sjavax\.ejb\.", contents)
    if(result!=None):
        logit(result)
        return "JavaJavaBeans"

    result = re.search(r"import\sorg\.hibernate\.", contents)
    if(result!=None):
        logit(result)
        return "JavaHibernate"

    result = re.search(r"import\sorg\.apache\.ibatis", contents)
    if(result!=None):
        logit(result)
        return "JavaMybatis"

    result = re.search(r"@interface\s[a-zA-Z]+\s?:\s?NSObject", contents)
    if(result!=None):
        logit(result)
        return "ObjCCoreData"

    result = re.search(r"using\sDapper", contents)
    if(result!=None):
        logit(result)
        return ".NETDapper"

    result = re.search(r"using\sSystem\.ComponentModel", contents)
    if(result!=None):
        logit(result)
        return ".NETEntityFramework"

    result = re.search(r"using\sSystem\.Data\.Linq", contents)
    if(result!=None):
        logit(result)
        return ".NETLinqToSQL"

    result = re.search(r"using\sNHibernate", contents)
    if(result!=None):
        logit(result)
        return ".NETNHibernate"

    result = re.search(r"use\sDoctrine\\ORM", contents)
    if(result!=None):
        logit(result)
        return "PhpDoctrine"

    result = re.search(r"use\sPropel", contents)
    if(result!=None):
        logit(result)
        return "PhpPropel"

    result = re.search(r"import\ssqlalchemy", contents)
    if(result!=None):
        logit(result)
        return "PhythonSQLAlchemy"

    result = re.search(r"from\sdjango|import\sdjango", contents)
    if(result!=None):
        logit(result)
        return "PhythonDjango"

    result = re.search(r"from\ssqlobject|import\ssqlobject", contents)
    if(result!=None):
        logit(result)
        return "PhythonSQLObject"

    #print("Nothing found.")
    #Utils.FileUtils.writeFile(logFile, "Nothing found.")
    return "NoORM"

def check_folder_for_orm(repo_root, dir, outFile):
    for root, dirs, files in os.walk(os.path.join(repo_root, dir)):
        files = [f for f in files if not f[0] == '.']
        dirs[:] = [d for d in dirs if not d[0] == '.']
        for file in files:
            result = check_file_for_orm(os.path.join(root,file))
            if(result!="NoORM"):
                FileUtils.writeFile(outFile, dir + "," + result + "\n")
                return
    FileUtils.writeFile(outFile, dir + "," + "NoORM\n")


