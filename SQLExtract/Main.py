import os
import re
import shutil
import sys
import SQLExtract
import SQLCleanser
import MetricsCalculator
import PLUsedMetrics
import AppNature
import FileUtils
import ORM_detector

#repoStoreRoot = "/Users/Tushar/Documents/Research/dbSmells/dbSmellData/qualitativeAnalysis/ReposQualitative/"
#repoResultRoot = "/Users/Tushar/Documents/Research/dbSmells/dbSmellData/qualitativeAnalysis/rq_sql_repo/"
#repoTempRoot = repoResultRoot + "temp/"
exclude_list = ["results", "sig_release-impact"]

def get_folder_paths():
    if len(sys.argv) <= 1:
        print ("Please provide path of the root folder containing projects to analyze.")
        sys.exit(1)
    repoStoreRoot = sys.argv[1]
    repoResultRoot = os.path.join(repoStoreRoot, "results")
    #print ("Result folder: " + repoResultRoot)
    if not os.path.exists(repoResultRoot):
        os.makedirs(repoResultRoot)
    repoTempRoot = os.path.join(repoResultRoot, "temp")
    #print("Temporary folder: " + repoTempRoot)
    if not os.path.exists(repoTempRoot):
        os.makedirs(repoTempRoot)
    return repoStoreRoot, repoResultRoot, repoTempRoot

def extract_sql_loose():
    # This part extracts the sql statements using slightly loose regular expressions
    print("Extracting SQL statement candidates...")
    logFile = repoTempRoot + os.sep + "log.txt"
    counter = 1
    for dir in os.listdir(repoStoreRoot):
        if os.path.isdir(os.path.join(repoStoreRoot, dir)):
            if str(dir) in exclude_list:
                continue
            print("Analyzing repo " + str(counter) + ": " + str(dir) + "\n")
            counter += 1
            sqlfile = os.path.join(repoTempRoot, dir + ".sql")
            if (os.path.isfile(sqlfile)):
                print("The repo is already analyzed ... skipping\n")
            else:
                SQLExtract.extractAllSQLCode(logFile, repoStoreRoot, repoTempRoot, dir)
    print("Extracting SQL statement candidates...Done")

def cleanse_sql():
    # This part takes the extracted sql statements from the previous step and cleanse it using stricter regex
    print("Cleansing extracted SQL statement candidates...")
    counter = 1
    for file in os.listdir(repoTempRoot):
        if file.endswith(".sql"):
            print(str(counter) + ":" + str(file))
            counter += 1
            if not os.path.exists(os.path.join(repoResultRoot, file)):
                print("...analyzing")
                with open(os.path.join(repoTempRoot, file), "r", errors='ignore') as r:
                    with open(os.path.join(repoResultRoot, file), "w", errors='ignore') as w:
                        for line in r:
                            line = line.strip()
                            line = re.sub(r' +', r' ', line)
                            if len(line) > 1000:
                                line = line[:1000]
                            newline = SQLCleanser.processLine(line)
                            if not newline == "":
                                w.write(str(newline) + "\n")
    print("Cleansing extracted SQL statement candidates...Done")

def delete_temp(folder):
    print("Removing temporary folder..")
    shutil.rmtree(folder)
    print("Done.")

def collect_metrics():
    print("Collecting basic SQL metrics...")
    resultFile = os.path.join(repoResultRoot, "metrics.csv")
    MetricsCalculator.writeFile(resultFile,
                                "repo,selectStmtCount,createStmtCount,insertStmtCount,updateStmtCount,createIndexStmtCount")
    counter = 1
    for file in os.listdir(repoResultRoot):
        if file.endswith(".sql"):
            #print(str(counter) + " analyzing " + str(file) + "...")
            counter += 1
            MetricsCalculator.computeAllMetrics(repoResultRoot, file, resultFile)
    print("Done")

def collect_prog_language_used_metrics():
    print("Collecting programming language used metrics...")
    resultFile = repoResultRoot + "/progLang.csv"

    PLUsedMetrics.writeFile(resultFile,
                            "repo,TotalFiles,java,cs,c,cxx,py,vb,php,jsx,pl,mm,rb,aspx,htmx,sql,pkb,TotalLOC")
    counter = 1
    for dir in os.listdir(repoStoreRoot):
        if os.path.isdir(os.path.join(repoStoreRoot, dir)):
            #print(str(counter) + " analyzing dir: " + str(dir))
            counter += 1
            PLUsedMetrics.computePLusedMetrics(repoStoreRoot, dir, resultFile)
    print("Done")
    return resultFile

def collect_app_nature_metrics():
    print("Collecting app nature metrics...")
    resultFile = AppNature.infer_app_nature(repoStoreRoot, repoResultRoot, plMetricsFile)
    print("Collecting app nature metrics...Done.")
    return resultFile

def collect_orm_data():
    print("Collecting ORM data...")
    outFile = repoResultRoot + "/orm.csv"
    counter = 1
    with open(app_nature_file, "r+", errors='ignore') as t:
        for tLine in t:
            splitLine = tLine.split(",")
            cur_dir = os.path.join(repoStoreRoot, splitLine[0])
            if os.path.isdir(cur_dir):
                print("Analyzing repo " + str(counter) + ": " + str(splitLine[0]) + "\n")
                #FileUtils.writeFile(logFile, "Analyzing repo " + str(counter) + ": " + str(splitLine[0]) + "\n")
                counter += 1
                ORM_detector.check_folder_for_orm(repoStoreRoot, splitLine[0], outFile)
    print("Collecting ORM data...Done.")


repoStoreRoot, repoResultRoot, repoTempRoot = get_folder_paths()
extract_sql_loose()
cleanse_sql()
delete_temp(repoTempRoot)
collect_metrics()
plMetricsFile = collect_prog_language_used_metrics()
app_nature_file = collect_app_nature_metrics()
collect_orm_data()
print("Done - Thank you.")

