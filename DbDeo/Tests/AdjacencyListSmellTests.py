from unittest import TestCase

from Model.MetaModel import MetaModel
from DbSmellDetector.SmellDetector import  SmellDetector
import os
from Utils import FileUtils
from DbSmellDetector import Constants

class AdjacencyListSmellTests(TestCase):
    def test_adjacencyList(self):
        root = "/Users/Tushar/Documents/Research/dbSmells/DbDeo/DbDeo/Tests/"
        file = "testSubject.sql"
        metaModel = MetaModel()
        metaModel.prepareMetaModel(root + file, root + "log.txt")
        smellDetector = SmellDetector(metaModel, root + "temp/", file)
        if(os.path.isfile(root + "temp/testSubject.txt")):
            os.remove(root + "temp/testSubject.txt")
        smellDetector.detectAllDbSmells()
        contents = FileUtils.readFileContents(root + "temp/testSubject.txt")
        self.assertIn("Detected: " + Constants.ADJACENCY_LIST, contents)