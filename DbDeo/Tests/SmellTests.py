from unittest import TestCase

from Model.MetaModel import MetaModel
from DbSmellDetector.SmellDetector import SmellDetector
import os
from Utils import FileUtils
from DbSmellDetector import Constants


class SmellTests(TestCase):

    def prepareTest(self, file):
        pwd = os.getcwd()
        root = pwd + "/Tests/"
        metaModel = MetaModel()
        fileTxt = file.replace(".sql", ".txt")
        metaModel.prepareMetaModel(root +"/"+ file, root + "log.txt")
        if not os.path.exists(root + '/temp'):
            os.makedirs(root + '/temp')
        smellDetector = SmellDetector(metaModel, root + "/temp/", file)
        if (os.path.isfile(root + "/temp/" + fileTxt)):
            os.remove(root + "/temp/" + fileTxt)
        smellDetector.detectAllDbSmells()
        return FileUtils.readFileContents(root + "/temp/" + fileTxt)

    def test_compoundAttributeSmell_variant1(self):
        contents = self.prepareTest("testSubject.sql")
        self.assertIn("Detected: " + Constants.COMPOUND_ATTRIBUTE_SMELL + " Variant: 1", contents)

    def test_compoundAttributeSmell_variant2(self):
        contents = self.prepareTest("testSubject.sql")
        self.assertIn("Detected: " + Constants.COMPOUND_ATTRIBUTE_SMELL + " Variant: 2", contents)

    def test_compoundAttributeSmell_variant3(self):
        contents = self.prepareTest("testSubject.sql")
        self.assertIn("Detected: " + Constants.COMPOUND_ATTRIBUTE_SMELL + " Variant: 3", contents)

    def test_adjacencyList(self):
        contents = self.prepareTest("testSubject.sql")
        self.assertIn("Detected: " + Constants.ADJACENCY_LIST, contents)

    def test_godTable(self):
        contents = self.prepareTest("testSubject.sql")
        self.assertIn("Detected: " + Constants.GOD_TABLE, contents)

    def test_valuesInColDef(self):
        contents = self.prepareTest("testSubject.sql")
        self.assertIn("Detected: " + Constants.VALUES_IN_COLUMN_DEFINION, contents)

    def test_metaDataAsData(self):
        contents = self.prepareTest("testSubject.sql")
        self.assertIn("Detected: " + Constants.METADATA_AS_DATA, contents)

    def test_multicolumnAttribute(self):
        contents = self.prepareTest("testSubject.sql")
        self.assertIn("Detected: " + Constants.MULTICOLUMN_ATTRIBUTE, contents)

    def test_cloneTables(self):
        contents = self.prepareTest("testSubject.sql")
        self.assertIn("Detected: " + Constants.CLONE_TABLES, contents)

    def test_duplicateColumns(self):
        contents = self.prepareTest("testSubject.sql")
        self.assertIn("Detected: " + Constants.DUPLICATE_COLUMN_NAMES, contents)

    def test_indexShotgun_variant1(self):
        contents = self.prepareTest("testSubject.sql")
        self.assertIn("Detected: " + Constants.INDEX_SHOTGUN + " Variant: 1", contents)

    def test_indexShotgun_variant2(self):
        contents = self.prepareTest("IndexShotgunTestSubject.sql")
        self.assertIn("Detected: " + Constants.INDEX_SHOTGUN + " Variant: 2", contents)

    def test_indexShotgun_variant3(self):
        contents = self.prepareTest("IndexShotgunTestSubject.sql")
        self.assertIn("Detected: " + Constants.INDEX_SHOTGUN + " Variant: 3", contents)

    def test_indexShotgun_variant3_negative(self):
        contents = self.prepareTest("IndexShotgunTestSubject_negative.sql")
        self.assertNotIn("Detected: " + Constants.INDEX_SHOTGUN + " Variant: 3", contents)
    
    def test_ObsoleteColumnTypes(self):
        contents = self.prepareTest("testSubject.sql")
        self.assertIn("Detected: " + Constants.OBSOLETE_COLUMN_TYPES, contents)
