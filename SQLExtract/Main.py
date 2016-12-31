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
        print("Analyzing repo " + str(counter) + ": " + str(dir))
        counter += 1
        SQLExtract.extractAllSQLCode(logFile, repoStoreRoot, repoResultRoot, dir)
