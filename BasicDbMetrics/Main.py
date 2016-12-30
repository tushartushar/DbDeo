import os
import sys
import MetricsCalculator

#repoStoreRoot = "/Users/Tushar/Documents/Workspace/SQLRepoDownload/resultRepos/"
repoResultRoot = sys.argv[1]
resultFile = repoResultRoot + "/metrics.csv"
MetricsCalculator.writeFile(resultFile, "repo,selectStmtCount,createStmtCount,insertStmtCount,updateStmtCount,createIndexStmtCount")

for file in os.listdir(repoResultRoot):
    if file.endswith(".sql"):
        MetricsCalculator.computeAllMetrics(repoResultRoot, file, resultFile)
