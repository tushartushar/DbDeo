import os
import sys
import MetricsCalculator

#repoResultRoot = "/Users/Tushar/Documents/Research/dbSmells/dbSmellData/resultReposCleansed"
repoResultRoot = sys.argv[1]
resultFile = repoResultRoot + "/metrics.csv"
#resultFile = "/Users/Tushar/Documents/Research/dbSmells/dbSmellData/metrics.csv"
MetricsCalculator.writeFile(resultFile, "repo,selectStmtCount,createStmtCount,insertStmtCount,updateStmtCount,createIndexStmtCount")

counter = 1
for file in os.listdir(repoResultRoot):
    if file.endswith(".sql"):
        print(str(counter) + " analyzing " + str(file) + "...")
        counter += 1
        MetricsCalculator.computeAllMetrics(repoResultRoot, file, resultFile)
        print("Done")
