from unittest import TestCase

from Model.MetaModel import MetaModel
from DbSmellDetector.SmellDetector import SmellDetector
import os
from Utils import FileUtils
from DbSmellDetector import Constants


class SmellTests(TestCase):
    def test_compoundAttributeSmell_variant1(self):
        root = "/Users/Tushar/Documents/Research/dbSmells/DbDeo/DbDeo/Tests/"
        file = "testSubject.sql"
        metaModel = MetaModel()
        metaModel.prepareMetaModel(root + file, root + "log.txt")
        smellDetector = SmellDetector(metaModel, root + "temp/", file)
        if (os.path.isfile(root + "temp/testSubject.txt")):
            os.remove(root + "temp/testSubject.txt")
        smellDetector.detectAllDbSmells()
        contents = FileUtils.readFileContents(root + "temp/testSubject.txt")
        self.assertIn("Detected: " + Constants.COMPOUND_ATTRIBUTE_SMELL + " Variant: 1", contents)

    def test_compoundAttributeSmell_variant2(self):
        root = "/Users/Tushar/Documents/Research/dbSmells/DbDeo/DbDeo/Tests/"
        file = "testSubject.sql"
        metaModel = MetaModel()
        metaModel.prepareMetaModel(root + file, root + "log.txt")
        smellDetector = SmellDetector(metaModel, root + "temp/", file)
        if (os.path.isfile(root + "temp/testSubject.txt")):
            os.remove(root + "temp/testSubject.txt")
        smellDetector.detectAllDbSmells()
        contents = FileUtils.readFileContents(root + "temp/testSubject.txt")
        self.assertIn("Detected: " + Constants.COMPOUND_ATTRIBUTE_SMELL + " Variant: 2", contents)

    def test_compoundAttributeSmell_variant3(self):
        root = "/Users/Tushar/Documents/Research/dbSmells/DbDeo/DbDeo/Tests/"
        file = "testSubject.sql"
        metaModel = MetaModel()
        metaModel.prepareMetaModel(root + file, root + "log.txt")
        smellDetector = SmellDetector(metaModel, root + "temp/", file)
        if (os.path.isfile(root + "temp/testSubject.txt")):
            os.remove(root + "temp/testSubject.txt")
        smellDetector.detectAllDbSmells()
        contents = FileUtils.readFileContents(root + "temp/testSubject.txt")
        self.assertIn("Detected: " + Constants.COMPOUND_ATTRIBUTE_SMELL + " Variant: 3", contents)

    def test_adjacencyList(self):
        root = "/Users/Tushar/Documents/Research/dbSmells/DbDeo/DbDeo/Tests/"
        file = "testSubject.sql"
        metaModel = MetaModel()
        metaModel.prepareMetaModel(root + file, root + "log.txt")
        smellDetector = SmellDetector(metaModel, root + "temp/", file)
        if (os.path.isfile(root + "temp/testSubject.txt")):
            os.remove(root + "temp/testSubject.txt")
        smellDetector.detectAllDbSmells()
        contents = FileUtils.readFileContents(root + "temp/testSubject.txt")
        self.assertIn("Detected: " + Constants.ADJACENCY_LIST, contents)

    def test_godTable(self):
        root = "/Users/Tushar/Documents/Research/dbSmells/DbDeo/DbDeo/Tests/"
        file = "testSubject.sql"
        metaModel = MetaModel()
        metaModel.prepareMetaModel(root + file, root + "log.txt")
        smellDetector = SmellDetector(metaModel, root + "temp/", file)
        if (os.path.isfile(root + "temp/testSubject.txt")):
            os.remove(root + "temp/testSubject.txt")
        smellDetector.detectAllDbSmells()
        contents = FileUtils.readFileContents(root + "temp/testSubject.txt")
        self.assertIn("Detected: " + Constants.GOD_TABLE, contents)

    def test_valuesInColDef(self):
        root = "/Users/Tushar/Documents/Research/dbSmells/DbDeo/DbDeo/Tests/"
        file = "testSubject.sql"
        metaModel = MetaModel()
        metaModel.prepareMetaModel(root + file, root + "log.txt")
        smellDetector = SmellDetector(metaModel, root + "temp/", file)
        if (os.path.isfile(root + "temp/testSubject.txt")):
            os.remove(root + "temp/testSubject.txt")
        smellDetector.detectAllDbSmells()
        contents = FileUtils.readFileContents(root + "temp/testSubject.txt")
        self.assertIn("Detected: " + Constants.VALUES_IN_COLUMN_DEFINION, contents)

    def test_metaDataAsData(self):
        root = "/Users/Tushar/Documents/Research/dbSmells/DbDeo/DbDeo/Tests/"
        file = "testSubject.sql"
        metaModel = MetaModel()
        metaModel.prepareMetaModel(root + file, root + "log.txt")
        smellDetector = SmellDetector(metaModel, root + "temp/", file)
        if (os.path.isfile(root + "temp/testSubject.txt")):
            os.remove(root + "temp/testSubject.txt")
        smellDetector.detectAllDbSmells()
        contents = FileUtils.readFileContents(root + "temp/testSubject.txt")
        self.assertIn("Detected: " + Constants.METADATA_AS_DATA, contents)

    def test_multicolumnAttribute(self):
        root = "/Users/Tushar/Documents/Research/dbSmells/DbDeo/DbDeo/Tests/"
        file = "testSubject.sql"
        metaModel = MetaModel()
        metaModel.prepareMetaModel(root + file, root + "log.txt")
        smellDetector = SmellDetector(metaModel, root + "temp/", file)
        if (os.path.isfile(root + "temp/testSubject.txt")):
            os.remove(root + "temp/testSubject.txt")
        smellDetector.detectAllDbSmells()
        contents = FileUtils.readFileContents(root + "temp/testSubject.txt")
        self.assertIn("Detected: " + Constants.MULTICOLUMN_ATTRIBUTE, contents)

    def test_cloneTables(self):
        root = "/Users/Tushar/Documents/Research/dbSmells/DbDeo/DbDeo/Tests/"
        file = "testSubject.sql"
        metaModel = MetaModel()
        metaModel.prepareMetaModel(root + file, root + "log.txt")
        smellDetector = SmellDetector(metaModel, root + "temp/", file)
        if (os.path.isfile(root + "temp/testSubject.txt")):
            os.remove(root + "temp/testSubject.txt")
        smellDetector.detectAllDbSmells()
        contents = FileUtils.readFileContents(root + "temp/testSubject.txt")
        self.assertIn("Detected: " + Constants.CLONE_TABLES, contents)

    def test_duplicateColumns(self):
        root = "/Users/Tushar/Documents/Research/dbSmells/DbDeo/DbDeo/Tests/"
        file = "testSubject.sql"
        metaModel = MetaModel()
        metaModel.prepareMetaModel(root + file, root + "log.txt")
        smellDetector = SmellDetector(metaModel, root + "temp/", file)
        if (os.path.isfile(root + "temp/testSubject.txt")):
            os.remove(root + "temp/testSubject.txt")
        smellDetector.detectAllDbSmells()
        contents = FileUtils.readFileContents(root + "temp/testSubject.txt")
        self.assertIn("Detected: " + Constants.DUPLICATE_COLUMN_NAMES, contents)