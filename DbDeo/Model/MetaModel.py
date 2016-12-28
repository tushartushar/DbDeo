from Model import SelectStmt, SQLParse
from Model.CreateStmt import CreateStmt
from Model.InsertStmt import InsertStmt
from Model.SQLStmtType import SQLStmtType
from Utils import FileUtils
from Model.UpdateStmt import UpdateStmt
from Model.CreateIndexStmt import CreateIndexStmt

class MetaModel(object):
    def __init__(self):
        self.selectStmtList = []
        self.createStmtList = []
        self.insertStmtList = []
        self.updateStmtList = []
        self.createIndexStmtList = []

    def prepareMetaModel(self, file, logFile):
        FileUtils.log(logFile, "Processing " + str(file))
        with open(file, 'r', errors='ignore') as f:
            for line in f:
                MetaModel.processLine(self, line, logFile)

    def processLine(self, inLine, logFile):
        line = inLine.strip('"')
        parsedStmt = SQLParse.SQLParse(line)
        if(parsedStmt.getStmtType()==SQLStmtType.SELECT):
            selectStmt = SelectStmt.SelectStmt(parsedStmt)
            selectStmt.populate()
            self.selectStmtList.append(selectStmt)
            return
        if(parsedStmt.getStmtType()==SQLStmtType.CREATE):
            createStmt = CreateStmt(parsedStmt)
            createStmt.populate()
            self.createStmtList.append(createStmt)
            return
        if(parsedStmt.getStmtType()==SQLStmtType.INSERT):
            insertStmt = InsertStmt(parsedStmt)
            insertStmt.populate()
            self.insertStmtList.append(insertStmt)
            return
        if(parsedStmt.getStmtType()==SQLStmtType.UPDATE):
            updateStmt = UpdateStmt(parsedStmt)
            updateStmt.populate()
            self.updateStmtList.append(updateStmt)
            return
        if parsedStmt.getStmtType() == SQLStmtType.CREATE_INDEX:
            createIndexStmt = CreateIndexStmt(parsedStmt)
            createIndexStmt.populate()
            self.createIndexStmtList.append(createIndexStmt)

    def getKeyList(self):
        keyList = []
        for createStmt in self.createStmtList:
            curKeyList = createStmt.getKeyList()
            if len(curKeyList) > 0:
                keyList.extend(curKeyList)
        return keyList

    def getAllIndexList(self):
        indexList = []
        for index in self.createIndexStmtList:
            for indexCol in index.indexColumnList:
                indexList.append([index.tableName, indexCol])
        return indexList

    def getAllAttributeUsedInSelect(self):
        result = []
        for select in self.selectStmtList:
            result.extend(select.attributesInWhereList)
        return result