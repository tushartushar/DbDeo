#This program computes number of files belonging to major programming language in a set of repositories

import os
import PLUsedMetrics

repoStoreRoot = "/Users/Tushar/Documents/Workspace/SQLRepoDownload/repos/"
resultFile = repoStoreRoot + "progLang.csv"


PLUsedMetrics.writeFile(resultFile, "repo,TotalFiles,java,cs,c,cxx,py,vb,php,jsx,pl,mm,rb,aspx,htmx,sql,pkb,TotalLOC")
for dir in os.listdir(repoStoreRoot):
    if os.path.isdir(os.path.join(repoStoreRoot, dir)):
        PLUsedMetrics.computePLusedMetrics(repoStoreRoot, dir, resultFile)
