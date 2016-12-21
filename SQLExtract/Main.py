import os
import SQLExtract

repoStoreRoot = "/Users/Tushar/Documents/Workspace/SQLRepoDownload/repos/"
repoResultRoot = "/Users/Tushar/Documents/Workspace/SQLRepoDownload/resultRepos/"
logFile = repoStoreRoot + "log.txt"
for dir in os.listdir(repoStoreRoot):
    if os.path.isdir(os.path.join(repoStoreRoot, dir)):
        print("Analyzing repo " + str(dir))
        SQLExtract.extractAllSQLCode(logFile, repoStoreRoot, repoResultRoot, dir)
