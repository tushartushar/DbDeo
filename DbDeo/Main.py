import os
from Model.MetaModel import MetaModel

repoStoreRoot = "/Users/Tushar/Documents/Workspace/SQLRepoDownload/resultRepos/"
resultFile = repoStoreRoot + "dbSmells.txt"
logFile = repoStoreRoot + "log.txt"


for file in os.listdir(repoStoreRoot):
    if file.endswith(".sql"):
        MetaModel().prepareMetaModel(os.path.join(repoStoreRoot, file), logFile)