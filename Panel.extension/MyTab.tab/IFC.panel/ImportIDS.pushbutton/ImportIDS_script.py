#! python3

### SATART of CODE ImportIDS ###
#Autor: Sascha Hostettler
#Datum: 20.05.2024
#Version: ?
#Beschrieb: 
#
#
### SATART of CODE ImportIDS ###
print('\n### SATART of CODE ImportIDS ###')
##############################################################################
import ifcopenshell
import ifctester
import json
import csv

#Meine ausgelagerten Module
from lib.SetUpPropertySetDefinition import SetUpIDSPropertySetDefinition
from lib.getRevitCategoryFromIFCmapping import getRevitCategoryFromIFCmapping
from lib.getInstanceListe import getInstanceListe

# Application Members von/für Revit
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application
##############################################################################
# Legt fest ob bei Abstrakten Klassen die Kindelemente gesucht und auf Categorien überführt werden
IncludeAbstractEntity = True

#Laden des zu importierenden IDS
inputPath = input("enter Path to IDS: ")

IDSName = inputPath.split("\\")[-1].split('.')[0]

ProjectFilePath = 'C:\\temp\\revit'

dbJsonFile = f'{ProjectFilePath}\\db.json'
IdsXmlFile = f'{ProjectFilePath}\\{IDSName}.xml'

IDSPropertySetDefinedFolderPath = "C:\\ProgramData\\Autodesk\\ApplicationPlugins\\IFC 2021.bundle\\Contents\\2021"
IDSPropertySetDefinedFileName = f'IDSPropertySetDefined_{IDSName}'

RevitIfcMappingFile = "C:\ProgramData\Autodesk\RVT 2024\Test_Msc_23-12-26_exportlayers-ifc-IAI.txt"

#Sample Pfad für Tests
SampleIdsPath = f'C:\\Users\\Sascha Hostettler\\OneDrive - FHNW\\FHNW_Msc_VDC\\_MSc_Thesis_IDS\\04_Data\\SampleData\\PoC-Sampels\\{IDSName}.xml'

#Erzeuge dbDataFrame
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

my_ids = ifctester.open(idsPath)
# print(f'65: {my_ids.info["title"]} ({my_ids.info["ifcVersion"]}) has been loaded\n')
# IfcSchema = ifcopenshell.schema_by_name(schema= my_ids.info["ifcVersion"], schema_version=None)
IfcSchema = ifcopenshell.schema_by_name('IFC4')

#oeffne RevitIfcMappingFile
IfcCategoryMappingFile = open(RevitIfcMappingFile, 'r', encoding="utf-16").readlines()


# Creat dataframe for IDSPropertySetDefined in Revit
try:
    RevitParameterMappingDataFrame = list( csv.reader(open(f'{IDSPropertySetDefinedFolderPath}\\{IDSPropertySetDefinedFileName}.txt', 'r', newline=''), delimiter='\t')  )
except:
    RevitParameterMappingDataFrame = []
    

##############################################################################


for specification in my_ids.specifications:
    for appli in specification.applicability:

        #keine Berücksichtigung des Predefined Typ -> dafür müssen während der Laufzeit neue Felder angelegt werden
        if appli.__class__.__name__ == "Entity": 
            
            if type(appli.name) == str:
                if IfcSchema.declaration_by_name(appli.name).is_abstract() == True and IncludeAbstractEntity == True:
                    #Falls gewollt wird in diesem Abschnitt zu einer Abstrakte IfcEntitaet alle ihre Kindklassen auf die Revit Kategorie überführt
                    EntityList = getInstanceListe(IfcSchema, EntityName)
                else:
                    EntityList = [appli.name]

            elif 'enumeration' in appli.name.options:
                EntityList = appli.name.options['enumeration']
                for entity in EntityList:
                    #Falls gewollt wird in diesem Abschnitt zu einer Abstrakte IfcEntitaet alle ihre Kindklassen auf die Revit Kategorie überführt
                    if IfcSchema.declaration_by_name(entity).is_abstract() == True and IncludeAbstractEntity == True:
                        EntityList.remove(entity)                   
                        for el in getInstanceListe(IfcSchema, EntityName):
                            EntityList.append(el)
                    else:
                        pass

            elif 'pattern' in appli.name.options:
                print('Funktion pattern in Applicablity ist noch in Arbeit')
                #Pattern kann hier eingepflegt werden: èber Regex alle Passenden Klassen finden und diese als liste übergeben
                pass
        
        # keine weiteren applicabilities definiert, das noch keine bedingungen eingetroffen sind umd Paramter anzulegen -> dafür müssen während der Laufzeit neue Parameter angelegt werden. 
            print(EntityList)
            for EntityName in EntityList:
                print()
                print(EntityName)
                print(IDSName)

                dbDataFrame[IDSName]['IfcMapping'].update({str(EntityName).upper() : getRevitCategoryFromIFCmapping(EntityName, IfcCategoryMappingFile)})
                
                print()
                print(dbDataFrame[IDSName])

                try:
                    ParamterList = dbDataFrame[IDSName]['IDSArg'][str(EntityName).upper()]
                except:
                    dbDataFrame[IDSName]['IDSArg'].update({str(EntityName).upper() : []})
                    ParamterList = dbDataFrame[IDSName]['IDSArg'][str(EntityName).upper()]
            

                for requ in specification.requirements:
                    
                    if requ.__class__.__name__ == "Attribute":
                        
                        requ.minOccurs = None
                        requ.maxOccurs = None

                        ParamterList.append(f'Ifc{requ.name}')
                        dbDataFrame[IDSName]['IDSArg'].update({str(EntityName).upper() : ParamterList})

                    elif requ.__class__.__name__ == "Property":

                        RevitParameterMappingDataFrame = SetUpIDSPropertySetDefinition(RevitParameterMappingDataFrame, EntityList, requ)
                        

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
