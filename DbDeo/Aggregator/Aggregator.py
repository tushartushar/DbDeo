import os
from DbSmellDetector import Constants


def aggregate_results(resultRoot, aggregatedFile):
    with open(aggregatedFile, "w", errors='ignore') as f:
        f.write("Repo,CompoundAttribute1,CompoundAttribute2,CompoundAttribute3,AdjacencyList,GodTable,ValuesInColDef,MetadataAsData,MulticolumnAttribute,CloneTables,DuplicateColumnNames,IndexShotgun1,IndexShotgun2,IndexShotgun3,ObsoleteColumnTypes\n")
        for file in os.listdir(resultRoot):
            CompoundAttribute1 = 0
            CompoundAttribute2 = 0
            CompoundAttribute3 = 0
            AdjacencyList =0
            GodTable =0
            ValuesInColDef = 0
            MetadataAsData = 0
            MulticolumnAttribute = 0
            CloneTables = 0
            DuplicateColumnNames = 0
            IndexShotgun1 = 0
            IndexShotgun2 = 0
            IndexShotgun3 = 0
            ObsoleteColumnTypes = 0

            if file.endswith(".txt") and (not file == "log.txt"):
                with open(os.path.join(resultRoot, file), "r", errors='ignore') as reader:
                    for line in reader:
                        if "Detected: " + Constants.COMPOUND_ATTRIBUTE_SMELL + " Variant: 1" in line:
                            CompoundAttribute1 += 1
                        if "Detected: " + Constants.COMPOUND_ATTRIBUTE_SMELL + " Variant: 2" in line:
                            CompoundAttribute2 += 1
                        if "Detected: " + Constants.COMPOUND_ATTRIBUTE_SMELL + " Variant: 3" in line:
                            CompoundAttribute3 += 1
                        if "Detected: " + Constants.ADJACENCY_LIST in line:
                            AdjacencyList += 1
                        if "Detected: " + Constants.GOD_TABLE in line:
                            GodTable += 1
                        if "Detected: " + Constants.VALUES_IN_COLUMN_DEFINION in line:
                            ValuesInColDef += 1
                        if "Detected: " + Constants.METADATA_AS_DATA in line:
                            MetadataAsData += 1
                        if "Detected: " + Constants.MULTICOLUMN_ATTRIBUTE in line:
                            MulticolumnAttribute += 1
                        if "Detected: " + Constants.CLONE_TABLES in line:
                            CloneTables += 1
                        if "Detected: " + Constants.DUPLICATE_COLUMN_NAMES in line:
                            DuplicateColumnNames += 1
                        if "Detected: " + Constants.INDEX_SHOTGUN + " Variant: 1" in line:
                            IndexShotgun1 += 1
                        if "Detected: " + Constants.INDEX_SHOTGUN + " Variant: 2" in line:
                            IndexShotgun2 += 1
                        if "Detected: " + Constants.INDEX_SHOTGUN + " Variant: 3" in line:
                            IndexShotgun3 += 1
                        if "Detected: " + Constants.OBSOLETE_COLUMN_TYPES in line:
                            ObsoleteColumnTypes += 1
                f.write(str(file)+","+str(CompoundAttribute1)+","+str(CompoundAttribute2)+","+str(CompoundAttribute3)+","+str(AdjacencyList)+","+
                        str(GodTable)+","+str(ValuesInColDef)+","+str(MetadataAsData)+","+str(MulticolumnAttribute)+","+str(CloneTables)+","+
                        str(DuplicateColumnNames)+","+str(IndexShotgun1)+","+str(IndexShotgun2)+","+str(IndexShotgun3)+","+str(ObsoleteColumnTypes)+"\n")