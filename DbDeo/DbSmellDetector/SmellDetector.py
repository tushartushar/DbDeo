import os
from Utils import FileUtils
from DbSmellDetector import Constants

class SmellDetector(object):
    def __init__(self, metaModel, resultRoot, file):
        self.metaModel = metaModel
        self.resultRoot = resultRoot
        self.file = file
        self.resultFile = os.path.join(resultRoot, file.replace(".sql", ".txt"))

    def detectAllDbSmells(self):
        self.detectCompoundAttribute()

    def detectCompoundAttribute(self):
        for selectStmt in self.metaModel.selectStmtList:
            if selectStmt.isRegexPresentInWhere():
                FileUtils.writeFile(self.resultFile, "Detected: " + Constants.COMPOUND_ATTRIBUTE_SMELL + " Variant: 1"
                                    + " Found in following statement: " + selectStmt.parsedStmt.stmt)