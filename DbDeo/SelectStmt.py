import SQLParse


class SelectStmt(object):
    def __init__(self, line):
        self.stmt = line
        parsedStmt = SQLParse.SQLParse(line)
