import sys
import os
from Model.MetaModel import MetaModel
from DbSmellDetector.SmellDetector import  SmellDetector

repoStoreRoot = "/Users/Tushar/Documents/Research/dbSmells/dbSmellData/resultReposCleansed"
resultRoot = "/Users/Tushar/Documents/Research/dbSmells/dbSmellData/results"
#repoResultRoot = sys.argv[1]
logFile = resultRoot + "/log.txt"


for file in os.listdir(repoStoreRoot):
    if file.endswith(".sql"):
        metaModel = MetaModel()
        metaModel.prepareMetaModel(os.path.join(repoStoreRoot, file), logFile)
        smellDetector = SmellDetector(metaModel, resultRoot, file)
        smellDetector.detectAllDbSmells()
