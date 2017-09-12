import os
import sys
import Utils.PrimaryKeyInfo
from DbSmellDetector.SmellDetector import SmellDetector
from Model.MetaModel import MetaModel
import shutil
import Aggregator.Aggregator

'''
repoStoreRoot = "/Users/Tushar/Documents/Research/dbSmells/newData/silo/cleansed"
resultRoot = "/Users/Tushar/Documents/Research/dbSmells/newData/silo/result"
#repoResultRoot = sys.argv[1]
logFile = resultRoot + "/log.txt"
'''
def get_folder_paths():
    if len(sys.argv) <= 1:
        print ("Please provide path of the root folder containing SQL statements files to analyze.")
        sys.exit(1)
    repoStoreRoot = sys.argv[1]
    repoResultRoot = os.path.join(repoStoreRoot, "dbSmellsData")
    #print ("Result folder: " + repoResultRoot)
    if os.path.exists(repoResultRoot):
        shutil.rmtree(repoResultRoot)
    os.makedirs(repoResultRoot)
    aggregated_result_file = os.path.join(repoResultRoot, "aggregated_results.csv")
    return repoStoreRoot, repoResultRoot, aggregated_result_file

def detect_db_smells():
    print("Detecting database schema smells...")
    counter = 1
    logFile = os.path.join(resultRoot, "dbdeo_log.txt")
    primary_key_file  = os.path.join(resultRoot, "primaryKeyInfo.csv")
    for file in os.listdir(repoStoreRoot):
        if file.endswith(".sql"):
            print(str(counter) + " : Analyzing " + str(file))
            counter += 1
            cur_out_file = file.strip(".sql") + ".txt"
            if os.path.exists(os.path.join(resultRoot, cur_out_file)):
                continue
            metaModel = MetaModel()
            metaModel.prepareMetaModel(os.path.join(repoStoreRoot, file), logFile)
            # just to extract primary key information
            Utils.PrimaryKeyInfo.printPrimaryKeyInfo(metaModel, primary_key_file)
            smellDetector = SmellDetector(metaModel, resultRoot, file)
            smellDetector.detectAllDbSmells()
    print("Detecting database schema smells...Done.")

def aggregate_results():
    print("Aggregating generated results...")
    Aggregator.Aggregator.aggregate_results(resultRoot, aggregated_result_file)
    print("Aggregating generated results...Done.")

repoStoreRoot, resultRoot, aggregated_result_file = get_folder_paths()
detect_db_smells()
aggregate_results()
print("Analysis complete. Thank you.")

