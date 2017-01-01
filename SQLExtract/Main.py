import os
import shutil
import sys
import SQLExtract

#repoStoreRoot = "/Users/Tushar/Documents/Workspace/SQLRepoDownload/repos/"
#repoResultRoot = "/Users/Tushar/Documents/Workspace/SQLRepoDownload/resultRepos/"
repoStoreRoot = sys.argv[1]
repoResultRoot = repoStoreRoot + '/resultRepos'
if os.path.exists(repoResultRoot):
    shutil.rmtree(repoResultRoot)
os.makedirs(repoResultRoot)

logFile = repoResultRoot + "/log.txt"
counter = 1
for dir in os.listdir(repoStoreRoot):
    if os.path.isdir(os.path.join(repoStoreRoot, dir)):
        print("Analyzing repo " + str(counter) + ": " + str(dir) + "\n")
        counter += 1
        if (os.path.isfile(os.path.join(repoResultRoot, dir + ".sql"))):
            print("The repo is already analyzed ... skipping\n")
        else:
            SQLExtract.extractAllSQLCode(logFile, repoStoreRoot, repoResultRoot, dir)
