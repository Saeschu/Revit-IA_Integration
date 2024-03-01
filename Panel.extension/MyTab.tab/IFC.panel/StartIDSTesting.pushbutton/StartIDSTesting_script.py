
##############################################################################
import json
from pyrevit.coreutils.ribbon import ICON_MEDIUM
from pyrevit import script

ConfigPath = "C:\\Users\\Sascha Hostettler\\Documents\\GitHub\\pyRevit-IDS_bSDD\\Revit-IA_Integration\\Panel.extension\\lib\\config.json"
with open(ConfigPath) as config:
    isChecking = json.load(config)
##############################################################################

SYNC_VIEW_ENV_VAR = 'SYNCVIEWACTIVE'

def toggle_state():
    """Toggle tool state"""
    new_state = not script.get_envvar(SYNC_VIEW_ENV_VAR)
    script.set_envvar(SYNC_VIEW_ENV_VAR, new_state)
    script.toggle_icon(new_state)

##############################################################################
# __Main__
    
if isChecking['IsIDSChecking'] == True:
    isChecking['IsIDSChecking'] = False
    toggle_state()
else:
    isChecking['IsIDSChecking'] = True
    toggle_state()

config = open(ConfigPath, "w")
jsonString = json.dumps(isChecking)

config.write(jsonString)
config.close()    


