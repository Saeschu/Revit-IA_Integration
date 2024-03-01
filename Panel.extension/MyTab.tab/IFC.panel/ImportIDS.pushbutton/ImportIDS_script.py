#! python3

### SATART of CODE ImportIDS ###
print('\n### SATART of CODE ImportIDS ###')
##############################################################################

# Import necesseray libraris
import ifcopenshell
import ifctester

import json
import csv

#My Moduls
from lib.SetUpPropertySetDefinition import SetUpIDSPropertySetDefinition
from lib.getRevitCategoryFromIFCmapping import getRevitCategoryFromIFCmapping

# Application Members
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application
##############################################################################

#load IDS
inputPath = input("enter Path to IDS: ")

IDSName = inputPath.split("\\")[-1].split('.')[0]

ProjectFilePath = 'C:\\temp\\revit'

dbJsonFile = f'{ProjectFilePath}\\db.json'
IdsXmlFile = f'{ProjectFilePath}\\{IDSName}.xml'

IDSPropertySetDefinedFolderPath = "C:\\ProgramData\\Autodesk\\ApplicationPlugins\\IFC 2021.bundle\\Contents\\2021"
IDSPropertySetDefinedFileName = f'IDSPropertySetDefined_{IDSName}'

RevitIfcMappingFile = "C:\ProgramData\Autodesk\RVT 2024\Test_Msc_23-12-26_exportlayers-ifc-IAI.txt"

#Sample for Testing
SampleIdsPath = f'C:\\Users\\Sascha Hostettler\\OneDrive - FHNW\\FHNW_Msc_VDC\\_MSc_Thesis_IDS\\04_Data\\SampleData\\PoC-Sampels\\{IDSName}.xml'

#Creat dbDataFrame
dbJsonObject = open(dbJsonFile, "r")
try:
    dbDataFrame = json.load(dbJsonObject)
    dbDataFrame.update({IDSName : {'IDSArg': {}, 'IfcMapping' : {}}})
except:
    dbDataFrame = {IDSName : {'IDSArg': {}, 'IfcMapping' : {}}}


if inputPath.upper() == "SAMPLE":
    idsPath = SampleIdsPath
else:
    idsPath = inputPath.split('"')[1].replace("\\", "\\\\")

print(idsPath)
# idsPath = SampleIdsPath
my_ids = ifctester.open(idsPath)
print(f'{my_ids.info["title"]} has been loaded\n')


#open RevitIfcMappingFile
IfcCategoryMappingFile = open(RevitIfcMappingFile, 'r', encoding="utf-16")

# Creat dataframe for IDSPropertySetDefined in Revit
try:
    RevitParameterMappingDataFrame = list( csv.reader(open(f'{IDSPropertySetDefinedFolderPath}\\{IDSPropertySetDefinedFileName}.txt', 'r', newline=''), delimiter='\t')  )
except:
    RevitParameterMappingDataFrame = []
    

##############################################################################


for specification in my_ids.specifications:
    for appli in specification.applicability:

        if appli.__class__.__name__ == "Entity": 
            # print(appli.name)
            # print(getRevitCategoryFromIFCmapping(appli.name, IfcCategoryMappingFile))

            dbDataFrame[IDSName]['IfcMapping'].update({str(appli.name).upper() : getRevitCategoryFromIFCmapping(appli.name, IfcCategoryMappingFile)})
            
            try:
                ParamterList = dbDataFrame[IDSName]['IDSArg'][str(appli.name).upper()]
            except:
                dbDataFrame[IDSName]['IDSArg'].update({str(appli.name).upper() : []})
                ParamterList = dbDataFrame[IDSName]['IDSArg'][str(appli.name).upper()]
            
            for requ in specification.requirements:
                
                if requ.__class__.__name__ == "Attribute":
                    
                    requ.minOccurs = None
                    requ.maxOccurs = None

                    ParamterList.append(f'Ifc{requ.name}')
                    dbDataFrame[IDSName]['IDSArg'].update({str(appli.name).upper() : ParamterList})

                elif requ.__class__.__name__ == "Property":

                    RevitParameterMappingDataFrame = SetUpIDSPropertySetDefinition(RevitParameterMappingDataFrame, appli.name, requ)
                    

                elif requ.__class__.__name__ == "Classification":
                    print('Requirement is at Facet Classification, Importing ist in Procress')


                elif requ.__class__.__name__ == "Parts":
                    print('Requirement is at Facet Parts, Importing ist in Procress')


                elif requ.__class__.__name__ == "Material":
                    print('Requirement is at Facet Parts, Importing ist in Procress')
            
                                    
                
##############################################################################
dbJsonObject = open(dbJsonFile, "w")
jsonString = json.dumps(dbDataFrame)
dbJsonObject.write(jsonString)
dbJsonObject.close()

csv_writer = csv.writer(open(f'{IDSPropertySetDefinedFolderPath}\\{IDSPropertySetDefinedFileName}.txt', 'w', newline=''), delimiter='\t', quotechar='\t', quoting=csv.QUOTE_MINIMAL)
csv_writer.writerows(RevitParameterMappingDataFrame)

my_ids.to_xml(IdsXmlFile)

############################################################################

print("\n##Attributzuordnung zu IfcEntitäten: ")
print(dbDataFrame)
print("\n##Revit PropertySet Definition und zuordnung zu IfcEntitäten: ")
for line in RevitParameterMappingDataFrame:
    print(line)
print("####")
### ENDE of CODE ###
print('\n### ENDE of CODE ###')
