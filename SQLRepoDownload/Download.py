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
