#! python3

### SATART of CODE ImportIDS ###
print('\n### SATART of CODE ImportIDS ###')
##############################################################################

# Import necesseray libraris
import ifctester
import json
import sys
import csv

#My Moduls
sys.path.append('./Panel.extension/lib')
# from mymodule import get_RevitElementFromIFCmapping

from lib.SetUpPropertySetDefinition import SetUpIDSPropertySetDefinition
from lib.getRevitElementFromIFCmapping import getRevitElementFromIFCmapping

##############################################################################


##############################################################################
#handeling db
IDSName = 'IDS'
ProjectFilePath = 'C:\\temp\\revit'

dbJsonFile = f'{ProjectFilePath}\\db.json'
IdsXmlFile = f'{ProjectFilePath}\\{IDSName}.xml'

RevitIfcMappingFile = "C:\ProgramData\Autodesk\RVT 2024\Test_Msc_23-12-26_exportlayers-ifc-IAI.txt"

IDSPropertySetDefinedFolderPath = "C:\\ProgramData\\Autodesk\\ApplicationPlugins\\IFC 2021.bundle\\Contents\\2021"
IDSPropertySetDefinedFileName = f'IDSPropertySetDefined_{IDSName}'


#Sample for Testing
SampleIdsPath = f'C:\\Users\\Sascha Hostettler\\OneDrive - FHNW\\FHNW_Msc_VDC\\_MSc_Thesis_IDS\\04_Data\\SampleData\\PoC-Sampels\\{IDSName}.xml'

#Creat dbDataFrame
dbJsonObject = open(dbJsonFile, "w")


#open IDS
inputPath = input("enter Path to IDS: ")
print(inputPath)

if len(inputPath) == 0:
    idsPath = SampleIdsPath
else:
    idsPath = inputPath


my_ids = ifctester.open(idsPath)
print(f'{my_ids.info["title"]} has been loaded')


#open RevitIfcMappingFile
IfcCategoryMappingFile = open(RevitIfcMappingFile, 'r', encoding= 'utf-16')

# Creat dataframe for IDSPropertySetDefined in Revit
RevitParameterMappingDataFrame = list( csv.reader(open(f'{IDSPropertySetDefinedFolderPath}\\{IDSPropertySetDefinedFileName}.txt', 'r', newline=''), delimiter='\t')  )

##############################################################################
EntityList = []
dbDataFrame = {'IDSArg': {}}
ParameterListe = []

##############################################################################

##__MAIN__##
for specification in my_ids.specifications:
    for appli in specification.applicability:
        ParamterList = []
        if appli.__class__.__name__ == "Entity": 
            EntityList.append(str(appli.name).upper())

            for requ in specification.requirements:
                
                if requ.__class__.__name__ == "Attribute":
                    ParamterList.append(f'Ifc{requ.name}')
                    requ.minOccurs = None
                    requ.maxOccurs = None

                elif requ.__class__.__name__ == "Property":
                    ParamterList.append(requ.name)
                    RevitParameterMappingDataFrame = SetUpIDSPropertySetDefinition(RevitParameterMappingDataFrame, appli.name, requ)
                    
                dbDataFrame['IDSArg'].update({str(appli.name).upper() : ParamterList})





##############################################################################

dbDataFrame['IDSArg'].update({'NewParamter' : ParamterList})
dbDataFrame["IfcCategoryMapping"] = getRevitElementFromIFCmapping(EntityList, IfcCategoryMappingFile)
jsonString = json.dumps(dbDataFrame)
dbJsonObject.write(jsonString)
dbJsonObject.close()

csv_writer = csv.writer(open(f'{IDSPropertySetDefinedFolderPath}\\{IDSPropertySetDefinedFileName}.txt', 'w', newline=''), delimiter='\t', quotechar='\t', quoting=csv.QUOTE_MINIMAL)
csv_writer.writerows(RevitParameterMappingDataFrame)

my_ids.to_xml(IdsXmlFile)

############################################################################

print("\n##Revit Categry mappingDict: ")
print(dbDataFrame["IfcCategoryMapping"])
print("####")
### ENDE of CODE ###
print('\n### ENDE of CODE ###')




