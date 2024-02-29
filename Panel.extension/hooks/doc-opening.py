#! python3

### SATART of CODE doc-opening ###
##############################################################################
# from pyrevit import EXEC_PARAMS, DB

import json
##############################################################################

IsIDScheckingPath = "C:\\temp\\revit\\IsIDSChecking.json"
#{"IsIDSChecking" : true}

with open(IsIDScheckingPath, 'r', encoding='utf-8') as json_file:
    isChecking = json.load(json_file)

print(isChecking)

isChecking['IsIDSChecking'] = False
print(isChecking)

with open(IsIDScheckingPath, 'w', encoding='utf-8') as json_file:
    json.dump(isChecking, json_file)
