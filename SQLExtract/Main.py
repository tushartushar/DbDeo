import os
import re
import shutil
import sys
import SQLExtract
import SQLCleanser

#repoStoreRoot = "/Users/Tushar/Documents/Research/dbSmells/dbSmellData/qualitativeAnalysis/ReposQualitative/"
#repoResultRoot = "/Users/Tushar/Documents/Research/dbSmells/dbSmellData/qualitativeAnalysis/rq_sql_repo/"
#repoTempRoot = repoResultRoot + "temp/"

def get_folder_paths():
    if len(sys.argv) <= 1:
        print ("Please provide path of the root folder containing projects to analyze.")
        sys.exit(1)
    repoStoreRoot = sys.argv[1]
    repoResultRoot = os.path.join(repoStoreRoot, "results")
    #print ("Result folder: " + repoResultRoot)
    if os.path.exists(repoResultRoot):
        shutil.rmtree(repoResultRoot)
    os.makedirs(repoResultRoot)
    repoTempRoot = os.path.join(repoResultRoot, "temp")
    #print("Temporary folder: " + repoTempRoot)
    if not os.path.exists(repoTempRoot):
        os.makedirs(repoTempRoot)
    return repoStoreRoot, repoResultRoot, repoTempRoot

def extract_sql_loose():
    # This part extracts the sql statements using slightly loose regular expressions
    logFile = repoTempRoot + os.sep + "log.txt"
    counter = 1
    for dir in os.listdir(repoStoreRoot):
        if os.path.isdir(os.path.join(repoStoreRoot, dir)):
            if str(dir) == "results":
                continue
            print("Analyzing repo " + str(counter) + ": " + str(dir) + "\n")
            counter += 1
            if (os.path.isfile(os.path.join(repoTempRoot, dir + ".sql"))):
                print("The repo is already analyzed ... skipping\n")
            else:
                SQLExtract.extractAllSQLCode(logFile, repoStoreRoot, repoTempRoot, dir)

def cleanse_sql():
    # This part takes the extracted sql statements from the previous step and cleanse it using stricter regex
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

repoStoreRoot, repoResultRoot, repoTempRoot = get_folder_paths()
extract_sql_loose()
cleanse_sql()
print("Done - Thank you.")






