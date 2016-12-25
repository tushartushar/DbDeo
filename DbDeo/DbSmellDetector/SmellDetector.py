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
        self.detectAdjacencyList()
        self.detectGodTable()
        self.detectValuesInColDef()

    def detectCompoundAttribute(self):
        for selectStmt in self.metaModel.selectStmtList:
            if selectStmt.isRegexPresentInWhere():
                FileUtils.writeFile(self.resultFile, "Detected: " + Constants.COMPOUND_ATTRIBUTE_SMELL + " Variant: 1"
                                    + " Found in following statement: " + selectStmt.parsedStmt.stmt)
        for insertStmt in self.metaModel.insertStmtList:
            if insertStmt.isContainsCompoundAttribute():
                FileUtils.writeFile(self.resultFile, "Detected: " + Constants.COMPOUND_ATTRIBUTE_SMELL + " Variant: 2"
                                    + " Found in following statement: " + insertStmt.parsedStmt.stmt)
        for updateStmt in self.metaModel.updateStmtList:
            if updateStmt.isContainsCommaInSet():
                FileUtils.writeFile(self.resultFile, "Detected: " + Constants.COMPOUND_ATTRIBUTE_SMELL + " Variant: 3"
                                    + " Found in following statement: " + updateStmt.parsedStmt.stmt)

    def detectAdjacencyList(self):
        for createStmt in self.metaModel.createStmtList:
            for columnObj in createStmt.columnList:
                if columnObj.isReferences:
                    if columnObj.referencedTable == createStmt.tableName:
                        FileUtils.writeFile(self.resultFile, "Detected: " + Constants.ADJACENCY_LIST
                                    + " Found in following statement: " + createStmt.parsedStmt.stmt)

    def detectGodTable(self):
        for createStmt in self.metaModel.createStmtList:
            if createStmt.getColumnCount() > Constants.GOD_TABLE_MAX_COLUMN_THRESHOLD:
                FileUtils.writeFile(self.resultFile, "Detected: " + Constants.GOD_TABLE
                                    + " Found in following statement: " + createStmt.parsedStmt.stmt)

    def detectValuesInColDef(self):
        for createStmt in self.metaModel.createStmtList:
            for columnObj in createStmt.columnList:
                if columnObj.areValuesConstrained:
                    FileUtils.writeFile(self.resultFile, "Detected: " + Constants.VALUES_IN_COLUMN_DEFINION
                                    + " Found in following statement: " + createStmt.parsedStmt.stmt)
