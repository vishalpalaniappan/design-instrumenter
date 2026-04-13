import logging
from pathlib import Path
from clp_logging.handlers import ClpKeyValuePairStreamHandler

import os, uuid

ADLI_EXECUTION_ID = str(uuid.uuid4())

path = Path(os.path.dirname(__file__)) / f"{ADLI_EXECUTION_ID}.clp.zst"
clp_handler = ClpKeyValuePairStreamHandler(open(path, "wb"))
logger = logging.getLogger("adli")
logger.setLevel(logging.INFO)
logger.addHandler(clp_handler)

class LoggingHelper:
    '''
        This class holds all the logging functions used by the 
        instrumented code during runtime. 
    '''

    def __init__(self):
        self.count = 0

    def logVariable(self, stmtId, behaviorId, name, value):
        entry = {}
        entry["stmtId"] = stmtId
        entry["behaviorId"] = behaviorId
        entry["type"] = "variable"
        entry["name"] = name
        entry["value"] = value
        logger.info(entry)

    def logBehavior(self, stmtId, name):
        entry = {}
        entry["stmtId"] = stmtId
        entry["type"] = "behavior"
        entry["name"] = name
        logger.info(entry)


adli = LoggingHelper()