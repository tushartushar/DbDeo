import sys
import os
from Model.MetaModel import MetaModel
from DbSmellDetector.SmellDetector import  SmellDetector

#repoStoreRoot = "/Users/Tushar/Documents/Research/dbSmells/dbSmellData/tempRepo"
#resultRoot = "/Users/Tushar/Documents/Research/dbSmells/dbSmellData/results"
repoResultRoot = sys.argv[1]
logFile = repoResultRoot + "/log.txt"


for file in os.listdir(repoResultRoot):
    if file.endswith(".sql"):
        metaModel = MetaModel()
        metaModel.prepareMetaModel(os.path.join(repoResultRoot, file), logFile)
        smellDetector = SmellDetector(metaModel, repoResultRoot, file)
        smellDetector.detectAllDbSmells()
