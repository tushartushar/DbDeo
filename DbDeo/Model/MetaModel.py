import FileUtils
import Model.SQLParse
from Model import SelectStmt, SQLParse
from Model.CreateStmt import CreateStmt
from Model.InsertStmt import InsertStmt
from Model.SQLStmtType import SQLStmtType


class MetaModel(object):
    def __init__(self):
        self.selectStmtList = []
        self.createStmtList = []
        self.insertStmtList = []

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
