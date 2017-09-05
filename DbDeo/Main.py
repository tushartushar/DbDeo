import os

import Utils.PrimaryKeyInfo
from DbSmellDetector.SmellDetector import SmellDetector
from MetaModel import MetaModel

repoStoreRoot = "/Users/Tushar/Documents/Research/dbSmells/newData/silo/cleansed"
resultRoot = "/Users/Tushar/Documents/Research/dbSmells/newData/silo/result"
#repoResultRoot = sys.argv[1]
logFile = resultRoot + "/log.txt"


counter = 1
for file in os.listdir(repoStoreRoot):
    if file.endswith(".sql"):
        print (str(counter) + " : Analyzing " + str(file))
        counter += 1
        cur_out_file = file.strip(".sql") + ".txt"
        if os.path.exists(os.path.join(resultRoot, cur_out_file)):
            continue
        metaModel = MetaModel()
        metaModel.prepareMetaModel(os.path.join(repoStoreRoot, file), logFile)
        #just to extract primary key information
        Utils.PrimaryKeyInfo.printPrimaryKeyInfo(metaModel)
        smellDetector = SmellDetector(metaModel, resultRoot, file)
        smellDetector.detectAllDbSmells()
