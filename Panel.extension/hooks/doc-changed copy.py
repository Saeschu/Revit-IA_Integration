#####IRONPYTHON####
import re
from pyrevit import EXEC_PARAMS, DB
from Autodesk.Revit.DB import *
import System
from System import Enum
import json

###https://help.autodesk.com/view/RVT/2024/ENU/?guid=Revit_API_Revit_API_Developers_Guide_Advanced_Topics_Events_Database_Events_DocumentChanged_event_html

event = EXEC_PARAMS.event_args.GetModifiedElementIds()
doc = EXEC_PARAMS.event_args.GetDocument()


#Imput Data from IDS/Json Import
dbPath = "C:\\TEMP\\revit\\db.json"
with open(dbPath) as file:
    ids = json.load(file)


if len(event) > 0:
    print(10*'-')
    print("EVENT  :", event)

    for elementId in event:

        print(type(elementId))
        element= doc.GetElement(elementId)
        cat = element.Category.BuiltInCategory
        print(cat)
        if str(cat) in ids['usedBuiltInCategory']:
            
            for param in element.Parameters:
                print(param.Definition.Name, " : ", param.AsString())


        
  
    print(10*'-') 