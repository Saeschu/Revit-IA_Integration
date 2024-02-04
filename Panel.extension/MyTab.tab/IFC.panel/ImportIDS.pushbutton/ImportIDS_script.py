#! python3

### SATART of CODE ImportIDS ###
print('\n### SATART of CODE ImportIDS ###')
##############################################################################
# Import necessary Revit API classes
# from Autodesk.Revit.DB import *
# import System
# from System import Enum
# import clr

# Import necesseray libraris for IDS
import ifcopenshell
import ifctester
# from tinydb import TinyDB, Query
import json
import sys

sys.path.append( '/Pnale.extenstion/lib')
from mymodule import get_RevitElementFromIFCmapping

##############################################################################
#handeling db
dbPath = "C:\\temp\\revit\\db.json"
idsxml = "C:\\temp\\revit\\ids.xml"

# Writing to sample.json
with open(dbPath, "w") as file:
    file.write("")


#open IDS
idsPath = input("enter Path to IDS: ")
print(idsPath)
idsPath = "C:\\Users\\Sascha Hostettler\\OneDrive - FHNW\\FHNW_Msc_VDC\\_MSc_Thesis_IDS\\04_Data\\SampleData\\PoC-Sampels\\IDS_SampleFM_Space_01.xml"

my_ids = ifctester.open(idsPath)

print(f'{my_ids.info["title"]} has been loaded')


#open IfcCategoryMapping
# print("ImportIFCCategoryTable :  ", app.ImportIFCCategoryTable) 
file_path = "C:\ProgramData\Autodesk\RVT 2024\Test_Msc_23-12-26_exportlayers-ifc-IAI.txt"
IfcCategoryMappingFile = open(file_path, 'r', encoding= 'utf-16')

##############################################################################
Entitylist = []
DictList = []
db = {'IDSArg': {}}

##############################################################################

##__MAIN__##
for specification in my_ids.specifications:
    for appli in specification.applicability:
        ParamterList = []
        if appli.__class__.__name__ == "Entity": 
            Entitylist.append(appli.name)

            for requ in specification.requirements:
                if requ.__class__.__name__ == "Attribute":
                    ParamterList.append(requ.name)
                    requ.minOccurs = None
                    requ.maxOccurs = None
                elif requ.__class__.__name__ == "Property":
                    ParamterList.append(requ.name)

                db['IDSArg'].update({appli.name : ParamterList})
                # DictList.append({appli.name : ParamterList})


# print(get_RevitElementFromIFCmapping(Entitylist, IfcCategoryMappingFile))
# db['IDSArg'] = DictList
db["IfcCategoryMapping"] = get_RevitElementFromIFCmapping(Entitylist, IfcCategoryMappingFile)
my_ids.to_xml(idsxml)

file = open(dbPath, "w")
jsonString = json.dumps(db)

file.write(jsonString)
file.close()
############################################################################


### ENDE of CODE ###
print('\n### ENDE of CODE ###')