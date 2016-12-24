from enum import Enum

class SQLStmtType(Enum):
    DEFAULT = 0
    SELECT = 1
    CREATE = 2
    INSERT = 3
    UPDATE = 4