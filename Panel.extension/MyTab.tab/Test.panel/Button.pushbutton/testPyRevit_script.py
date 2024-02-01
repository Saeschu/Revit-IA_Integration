
##Test Pyrevit###
print('### START ###')
#############################################################################
from pyrevit import revit, DB
from pyrevit import forms,script, EXEC_PARAMS
from pyrevit.forms import WPFWindow
from Autodesk.Revit.DB import *
import System
from System import Enum
import sys
import clr
import json
import time
##############################################################################

##############################################################################
# Application Members
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application
##############################################################################



# ElementID = ElementId(179398) #IfcName: Wand 1

# element = doc.GetElement(ElementID)
# ElementParameter = element.Parameters
# print(element)
# print(ElementParameter)

# for param in ElementParameter:
#     print(param.Name)

#Get Element by Filter
# all_Rooms = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Rooms).WhereElementIsNotElementType().ToElements()


# n= 0

# while n < 3:
#     print(10*'-')


#     print(app.DocumentChanged)
#     print(doc.GetModifiedElementIds())
    
#     for Rooms in all_Rooms:
        
# #Get Shared Paramter
#         sp_Name = Rooms.LookupParameter('Name')
#         print(sp_Name.AsString())
    
    
    # print(10*'-')    
    # n = n + 1

    # time.sleep(5)






##############################################################################
print('### ENDE ###')

















#############################################################################
# print(DB.LabelUtils.GetLabelFor(BuiltInCategory.OST_Rooms))

# for cat in System.Enum.GetValues(DB.BuiltInCategory):
    # print(cat)

# print(sys.version)
# print("\n##.sys.path:")
# print('\n'.join(sys.path))

# def print_html(output_str):
#     print(output_str.replace('<', '&clt;').replace('>', '&cgt;'))
# #clr.AddReference('Autodesk.Revit.DB')
# # import Autodesk.Revit.DB as DB

# print('\n## UIApplication:')



# print(__revit__)

# # cl = DB.FilteredElementCollector(__revit__.ActiveUIDocument.Document)\
# #         .OfClass(DB.Wall)\
# #         .WhereElementIsNotElementType()\
# #         .ToElements()


# # print('\n## list of DB.Walls:')
# # for wall in cl:
# #     print(f'{wall} id:{wall.Id.IntegerValue}')


# print('\n## Output from csv')
# import csv
# csvfile = csv.reader(open("C:\\TEMP\\revit\\csv.csv", 'rb'), delimiter=';')

# for row in csvfile:
#     print(row)

# import json
# jsonfile = json.load(open("C:\\TEMP\\bsdd\\db.json"))

# print(jsonfile)



