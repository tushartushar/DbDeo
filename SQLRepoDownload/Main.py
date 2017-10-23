from github import Github
import SQLCodeChecker
import shutil
import random
import time
import os
import FileUtils
from subprocess import call

def downloadRepo(github, repoName, repoStoreRoot, logFile):
    fullRepoName = "https://github.com/" + repoName + ".git"
    os.chdir(repoStoreRoot)
    folderName = repoName.replace("/", "_")
    if not os.path.isdir(os.path.join(repoStoreRoot, folderName)):
        FileUtils.log(logFile, "cloning: " + fullRepoName)
        os.mkdir(folderName)
        try:
            call(["git", "clone", "--depth=1", fullRepoName, folderName])
        except:
            print("Exception occurred!!")
            pass


repoInputFile = "/Users/User1/reposWithScore10.csv"
repoStoreRoot = "/Users/User1/SQLRepoDownload/repos/"
repoTempStoreRoot = repoStoreRoot
logFile = repoStoreRoot + "log.txt"

g = Github("githubDownloader", "useyourpassword")
file = open(repoInputFile, 'rt', errors='ignore')

for line in file.readlines():
    repoName = line.strip('\n')
    if not repoName == "":
        folderName = repoName.replace("/", "_")
        if(os.path.isdir(os.path.join(repoTempStoreRoot, folderName))):
            FileUtils.log(logFile, "Copying from temporary store " + folderName)
            try:
                shutil.copytree(os.path.join(repoTempStoreRoot, folderName), os.path.join(repoStoreRoot, folderName))
            except:
                pass
        else:
            fullFolderPath = os.path.join(repoStoreRoot, folderName)
            downloadRepo(g, repoName, repoStoreRoot, logFile)
            if(not SQLCodeChecker.IsRepoHaveSQLCode(fullFolderPath, logFile)):
                if(os.path.isdir(fullFolderPath)):
                    FileUtils.log(logFile, "Deleting " + fullFolderPath)
                    shutil.rmtree(fullFolderPath)
            n = random.randint(10,60)
            FileUtils.log(logFile, "Waiting for " + str(n) + " secs")
            time.sleep(n)
