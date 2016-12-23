from unittest import TestCase

from Model.MetaModel import MetaModel
from DbSmellDetector.SmellDetector import  SmellDetector
import os
from Utils import FileUtils
from DbSmellDetector import Constants

class CompoundAttributeSmellTests(TestCase):
    def test_variant1(self):
        root = "/Users/Tushar/Documents/Research/dbSmells/DbDeo/DbDeo/Tests/"
        file = "testSubject.sql"
        metaModel = MetaModel()
        metaModel.prepareMetaModel(root + file, root + "log.txt")
        smellDetector = SmellDetector(metaModel, root + "temp/", file)
        if(os.path.isfile(root + "temp/testSubject.txt")):
            os.remove(root + "temp/testSubject.txt")
        smellDetector.detectAllDbSmells()
        contents = FileUtils.readFileContents(root + "temp/testSubject.txt")
        self.assertIn("Detected: " + Constants.COMPOUND_ATTRIBUTE_SMELL + " Variant: 1", contents)

    def test_variant2(self):
        root = "/Users/Tushar/Documents/Research/dbSmells/DbDeo/DbDeo/Tests/"
        file = "testSubject.sql"
        metaModel = MetaModel()
        metaModel.prepareMetaModel(root + file, root + "log.txt")
        smellDetector = SmellDetector(metaModel, root + "temp/", file)
        if(os.path.isfile(root + "temp/testSubject.txt")):
            os.remove(root + "temp/testSubject.txt")
        smellDetector.detectAllDbSmells()
        contents = FileUtils.readFileContents(root + "temp/testSubject.txt")
        self.assertIn("Detected: " + Constants.COMPOUND_ATTRIBUTE_SMELL + " Variant: 2", contents)