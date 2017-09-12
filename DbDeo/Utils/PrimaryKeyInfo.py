import Utils.FileUtils

def printPrimaryKeyInfo(metaModel, outputFile):
    for createTableStmt in metaModel.createStmtList:
        for column in createTableStmt.columnList:
            if column.isPrimaryKey == True:
                if column.columnName == "":
                    for item in column.referencedColumnList:
                        line = ""
                        for col in createTableStmt.columnList:
                            if col.columnName == item:
                                line = item + "," + col.shortColumnType + "," + col.columnType
                                break
                        if line == "":
                            line = item + ",,"
                        Utils.FileUtils.writeFile(outputFile, line)
                else:
                    line = column.columnName + "," + column.shortColumnType + "," + column.columnType
                    Utils.FileUtils.writeFile(outputFile, line)