import os
import MetricsCalculator

repoStoreRoot = "/Users/Tushar/Documents/Workspace/SQLRepoDownload/resultRepos/"
resultFile = repoStoreRoot + "metrics.csv"
MetricsCalculator.writeFile(resultFile, "repo,selectStmtCount,createStmtCount,insertStmtCount")

for file in os.listdir(repoStoreRoot):
    if file.endswith(".sql"):
        MetricsCalculator.computeAllMetrics(repoStoreRoot, file, resultFile)