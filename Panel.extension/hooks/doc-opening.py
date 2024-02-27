### SATART of CODE doc-opening ###
##############################################################################
from pyrevit import EXEC_PARAMS, DB

import json
##############################################################################

IsIDScheckingPath = "C:\\temp\\revit\\IsIDSChecking.json"


with open(IsIDScheckingPath) as IsIDSchecking:
    isChecking = json.load(IsIDSchecking)

    isChecking['IsIDSChecking'] = False

jsonString = json.dumps(isChecking)

IsIDSchecking.write(jsonString)
IsIDSchecking.close() 

