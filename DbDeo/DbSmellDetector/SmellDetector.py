import os
import re

import Model.DataTypeConstants as Datatypes
from DbSmellDetector import Constants


class SmellDetector(object):
    def __init__(self, metaModel, resultRoot, file):
        self.metaModel = metaModel
        self.resultRoot = resultRoot
        self.file = file
        self.resultFile = os.path.join(resultRoot, file.replace(".sql", ".txt"))

    def detectAllDbSmells(self):
        self.smells = set()
        self.detectCompoundAttribute()
        self.detectAdjacencyList()
        self.detectGodTable()
        self.detectValuesInColDef()
        self.detectMetadataAsData()
        self.detectMulticolumnAttribute()
        self.detectCloneTables()
        self.detectDuplicateColumnNames()
        self.detectIndexShotgun()
        self.detectObsoleteColumnTypes()
        f = open(self.resultFile, "a", errors='ignore')
        for text in self.smells:
            f.write(text + "\n")
        f.close()

    def detectCompoundAttribute(self):
        for selectStmt in self.metaModel.selectStmtList:
            if selectStmt.isRegexPresentInWhere():
                self.smells.add("Detected: " + Constants.COMPOUND_ATTRIBUTE_SMELL + " Variant: 1"
                                )#+ " Found in following statement: " + selectStmt.parsedStmt.stmt)
        for insertStmt in self.metaModel.insertStmtList:
            if insertStmt.isContainsCompoundAttribute():
                self.smells.add("Detected: " + Constants.COMPOUND_ATTRIBUTE_SMELL + " Variant: 2"
                                )#+ " Found in following statement: " + insertStmt.parsedStmt.stmt)
        for updateStmt in self.metaModel.updateStmtList:
            if updateStmt.isContainsCommaInSet():
                self.smells.add("Detected: " + Constants.COMPOUND_ATTRIBUTE_SMELL + " Variant: 3"
                                )#+ " Found in following statement: " + updateStmt.parsedStmt.stmt)

    def detectAdjacencyList(self):
        for createStmt in self.metaModel.createStmtList:
            for columnObj in createStmt.columnList:
                if columnObj.isReferences:
                    if columnObj.referencedTable == createStmt.tableName:
                        self.smells.add("Detected: " + Constants.ADJACENCY_LIST
                                        )#+ " Found in following statement: " + createStmt.parsedStmt.stmt)
    def detectGodTable(self):
        for createStmt in self.metaModel.createStmtList:
            if createStmt.getColumnCount() > Constants.GOD_TABLE_MAX_COLUMN_THRESHOLD:
                self.smells.add("Detected: " + Constants.GOD_TABLE
                                )#+ " Found in following statement: " + createStmt.parsedStmt.stmt)
    def detectValuesInColDef(self):
        for createStmt in self.metaModel.createStmtList:
            for columnObj in createStmt.columnList:
                if columnObj.areValuesConstrained:
                    self.smells.add("Detected: " + Constants.VALUES_IN_COLUMN_DEFINION
                                    )#+ " Found in following statement: " + createStmt.parsedStmt.stmt)
    def detectMetadataAsData(self):
        for createStmt in self.metaModel.createStmtList:
            if not createStmt.getColumnCount() == 3:
                continue
            varCharColumnCount =0
            for columnObj in createStmt.columnList:
                if not columnObj.isConstraint:
                    if 'VARCHAR' in columnObj.columnType.upper():
                        varCharColumnCount += 1
            if varCharColumnCount >= 2:
                self.smells.add("Detected: " + Constants.METADATA_AS_DATA
                                )#+ " Found in following statement: " + createStmt.parsedStmt.stmt)

    def detectMulticolumnAttribute(self):
        for createStmt in self.metaModel.createStmtList:
            found = False
            for columnObj in createStmt.columnList:
                m = re.search(r'([a-zA-Z_]+)d*', columnObj.columnName)
                if not m == None:
                    if not m.group(1) == None:
                        #search the similar column name that only differs in the number
                        for colObj in createStmt.columnList:
                            if not columnObj == colObj:
                                searchStr = r'(' + m.group(1) + ')\d+'
                                k = re.search(searchStr, colObj.columnName)
                                if not k == None:
                                    self.smells.add("Detected: " + Constants.MULTICOLUMN_ATTRIBUTE
                                                    )#+ " Found in following statement: " + createStmt.parsedStmt.stmt)
                                    found = True
                                    break
                if found:
                    break

    def detectCloneTables(self):
        for createStmt in self.metaModel.createStmtList:
            m = re.search(r'([a-zA-Z_]+)d*', createStmt.tableName)
            if not m == None:
                if not m.group(1) == None:
                    #search the similar table names that only differs in the number
                    for cTableStmt in self.metaModel.createStmtList:
                        if not createStmt == cTableStmt:
                            #In certain cases, a table is repeated (with same name) with slight difference. This check eliminates that case
                            if not createStmt.tableName == cTableStmt.tableName:
                                searchStr = r'^(' + m.group(1) + ')\d+$'
                                k = re.search(searchStr, cTableStmt.tableName)
                                if not k == None:
                                    self.smells.add("Detected: " + Constants.CLONE_TABLES
                                                    )#+ " Found in following statement: " + createStmt.parsedStmt.stmt)

    def detectDuplicateColumnNames(self):
        listOfDuplicates = []
        for createStmt in self.metaModel.createStmtList:
            for columnObj in createStmt.columnList:
                if columnObj.isConstraint:
                    continue
                #Now, look for the similar column in all the column definitions
                for ctStmt in self.metaModel.createStmtList:
                    #In certain cases, a table is repeated (with same name) with slight difference. This check eliminates that case
                    if createStmt.tableName == ctStmt.tableName:
                        continue
                    for colObj in ctStmt.columnList:
                        if colObj.isConstraint:
                            continue
                        if not colObj == columnObj:
                            if colObj.columnName == columnObj.columnName:
                                if not colObj.shortColumnType == columnObj.shortColumnType:
                                    if not (colObj in listOfDuplicates or columnObj in listOfDuplicates):
                                        self.smells.add("Detected: " + Constants.DUPLICATE_COLUMN_NAMES
                                                        )#+ " Found in following statement: " + createStmt.parsedStmt.stmt +
                                                        #    " in following column " + columnObj.columnName +
                                                        #    " and in column " + colObj.columnName + " of table " + ctStmt.tableName)
                                    if not colObj in listOfDuplicates:
                                        listOfDuplicates.append(colObj)
                                    if not columnObj in listOfDuplicates:
                                        listOfDuplicates.append(columnObj)

    def detectIndexShotgun(self):
        self.detectIndexShotgun_variant1() #No index
        #most of the database vendors supports indexes for primary keys implicitly, so we only check the second variant for foreign keys
        self.detectIndexShotgun_variant2() #Insufficient index
        self.detectIndexShotgun_variant3() #Unused index

    def detectIndexShotgun_variant2(self):
        # detecting variant 2: Insufficient indexes
        keyList = self.metaModel.getForeignKeyList()  # keyList will contain 'table name, attribute name in (foreign) key' tuples
        indexList = self.metaModel.getAllIndexList()  # indexList will contain 'table name, attribute' tuple
        for keyItem in keyList:
            if not keyItem in indexList:
                self.smells.add("Detected: " + Constants.INDEX_SHOTGUN + " Variant: 2"
                                )#+ " Missing index for the primary/foreign key : " + str(keyItem))

    def detectIndexShotgun_variant1(self):
        if len(self.metaModel.createIndexStmtList) == 0:
            #added this check to avoid false positive
            if len(self.metaModel.createStmtList) > 0:
                self.smells.add("Detected: " + Constants.INDEX_SHOTGUN + " Variant: 1")

    def detectIndexShotgun_variant3(self):
        usedAttributesInAllSelect = self.metaModel.getAllAttributeUsedInSelect()
        indexList = self.metaModel.getAllIndexList()
        for index in indexList:
            if not index in usedAttributesInAllSelect:
                self.smells.add("Detected: " + Constants.INDEX_SHOTGUN + " Variant: 3"
                                )#+ " Following index not used : " + str(index))

    def detectObsoleteColumnTypes(self):
        listOfObsoletes = []
        for createStmt in self.metaModel.createStmtList:
            for columnObj in createStmt.columnList:
                shortType = columnObj.shortColumnType
                if shortType == Datatypes.TEXT or shortType == Datatypes.NTEXT or shortType == Datatypes.FLOAT or shortType == Datatypes.REAL:
                    self.smells.add("Detected: " +
                            Constants.OBSOLETE_COLUMN_TYPES )#+
                            #"Found in following statement: " +
                            #createStmt.parsedStmt.stmt +
                            #" in following column " + columnObj.columnName +
                            #" of table " + createStmt.tableName)
                    if not columnObj in listOfObsoletes:
                        listOfObsoletes.append(columnObj)

