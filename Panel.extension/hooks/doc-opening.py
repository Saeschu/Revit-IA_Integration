#! python3

### SATART of CODE doc-opening ###
##############################################################################
# from pyrevit import EXEC_PARAMS, DB

import json
import os

##############################################################################

IsIDScheckingPath = "C:\\Users\\Sascha Hostettler\\Documents\\GitHub\\pyRevit-IDS_bSDD\\Revit-IA_Integration\\Panel.extension\\lib\\config.json"
#{"IsIDSChecking" : true}

with open(IsIDScheckingPath, 'r', encoding='utf-8') as json_file:
    isChecking = json.load(json_file)

print('is Checking : ' + str(isChecking['IsIDSChecking']))

isChecking['IsIDSChecking'] = False
print('is Checking : ' + str(isChecking['IsIDSChecking']))

with open(IsIDScheckingPath, 'w', encoding='utf-8') as json_file:
    json.dump(isChecking, json_file)
