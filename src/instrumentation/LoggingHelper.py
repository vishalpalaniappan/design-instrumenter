import logging
import traceback
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

    def logVariable(self, stmtId, behaviorId, participantName, participantValue):
        entry = {}
        entry["type"] = "variable"
        entry["stmtId"] = stmtId
        entry["behaviorName"] = behaviorId
        entry["participantName"] = participantName
        entry["participantValue"] = participantValue
        logger.info(entry)

    def logBehavior(self, stmtId, behaviorId):
        entry = {}
        entry["type"] = "behavior"
        entry["stmtId"] = stmtId
        entry["behaviorName"] = behaviorId
        logger.info(entry)

    def logException(self, e, stmtId, behaviorId):
        entry = {}
        entry["type"] = "exception"
        entry["stmtId"] = stmtId
        entry["message"] = str(e)
        entry["traceback"] = traceback.format_exception(type(e), e, e.__traceback__)
        entry["behaviorName"] = behaviorId
        entry["exceptionType"] = type(e).__name__
        logger.info(entry)


adli = LoggingHelper()

adli.logException(Exception("Test Exception"), "test_stmt_id", "test_behavior_id")