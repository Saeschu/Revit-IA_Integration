
##############################################################################
import json
from pyrevit.coreutils.ribbon import ICON_MEDIUM
from pyrevit import script


config = script.get_config()
##############################################################################
IsIDScheckingPath = "C:\\temp\\revit\\IsIDSChecking.json"

# def __selfinit__(script_cmp, ui_button_cmp, __rvt__):
#     off_icon = script_cmp.get_bundle_file('off.png')
#     ui_button_cmp.set_icon(off_icon, icon_size=ICON_MEDIUM)

SYNC_VIEW_ENV_VAR = 'SYNCVIEWACTIVE'

def toggle_state():
    """Toggle tool state"""
    new_state = not script.get_envvar(SYNC_VIEW_ENV_VAR)
    # remove last datafile on start
    script.set_envvar(SYNC_VIEW_ENV_VAR, new_state)
    script.toggle_icon(new_state)

with open(IsIDScheckingPath) as IsIDSchecking:
    isChecking = json.load(IsIDSchecking)
   

if isChecking['IsIDSChecking'] == True:
    isChecking['IsIDSChecking'] = False
    
    toggle_state()

else:
    isChecking['IsIDSChecking'] = True
    toggle_state()
    
# print(isChecking['IsIDSChecking'])


IsIDSchecking = open(IsIDScheckingPath, "w")
jsonString = json.dumps(isChecking)

IsIDSchecking.write(jsonString)
IsIDSchecking.close()    


