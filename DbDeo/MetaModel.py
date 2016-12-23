import FileUtils
import SelectStmt


class MetaModel(object):
    metaModelObject = []
    def prepareMetaModel(self, file, logFile):
        FileUtils.log(logFile, "Processing " + str(file))
        with open(file, 'r', errors='ignore') as f:
            for line in f:
                MetaModel.processLine(self, line, logFile)

    def processLine(self, inLine, logFile):
        line = inLine.strip('"')
        #if(isSelectStmt(line)):
        selectStmt = SelectStmt.SelectStmt(line)

