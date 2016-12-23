import os
from Model.MetaModel import MetaModel
from DbSmellDetector.SmellDetector import  SmellDetector

repoStoreRoot = "/Users/Tushar/Documents/Workspace/SQLRepoDownload/resultRepos/"
resultRoot = "/Users/Tushar/Documents/Workspace/SQLRepoDownload/smellResult/"
logFile = repoStoreRoot + "log.txt"


for file in os.listdir(repoStoreRoot):
    if file.endswith(".sql"):
        metaModel = MetaModel()
        metaModel.prepareMetaModel(os.path.join(repoStoreRoot, file), logFile)
        smellDetector = SmellDetector(metaModel, resultRoot, file)
        smellDetector.detectAllDbSmells()