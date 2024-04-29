#! python3
### SATART of CODE getRequirements ###
#Autor: Sascha Hostettler
#Datum: 20.05.2024
#Version: ?
#Beschrieb: 
#
#
### SATART of CODE ImportIDS ###
# print('\n### SATART of CODE ImportIDS ###')
#############################################################################
import json
from lib.bSDDRequest import getbSDDRequest
import ifctester
import os

from pyrevit import EXEC_PARAMS, DB
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
import System
from System import Enum

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application

##############################################################################

def getImportedIDS():
    directory = 'C:\\temp\\revit'
    ImportedIDS = []
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            if str(filename).endswith('.xml'):
                ImportedIDS.append(filename.split('.')[0])

    return ImportedIDS 

#Check Requirements
## ToDo: Ergaenzen Mapping von requ.name auf Parameterbezeichnung (einbau Func getIfcPropertyName)
def getRequirements(requ, appliName):

    print(f'All {appliName} data')

    if requ.__class__.__name__ == "Attribute":
        if requ.value != None:                                            
            if requ.get_usage() == 'required':
                print(f'The {requ.name} shall be {requ.value}')

            elif requ.get_usage() == 'prohibited':
                print(f'The {requ.name} shall not be {requ.value}')
            
        else:
            if requ.get_usage() == 'required':
                print(f'The {requ.name} shall be provided')

            elif requ.get_usage() == 'prohibited':
                print(f'The {requ.name} shall not be provided')


    elif requ.__class__.__name__ == "Property":       
        if requ.value != None:                                            
            if requ.get_usage() == 'required':
                print(f'{requ.name} data shall be {requ.value} and in the dataset {requ.propertySet}')

            elif requ.get_usage() == 'prohibited':
                print(f'{requ.name} data shall not be {requ.value} and in the dataset {requ.propertySet}')
            
        else:
            if requ.get_usage() == 'required':
                print(f'{requ.name} data shall be provided in the dataset {requ.propertySet}')

            elif requ.get_usage() == 'prohibited':
                print(f'{requ.name} data shall not be provided in the dataset {requ.propertySet}')
        

    elif requ.__class__.__name__ == "Classification":
        if requ.value != None:                                            
            if requ.get_usage() == 'required':
                print(f'Shall have a {requ.system} reference of {requ.value}')

            elif requ.get_usage() == 'prohibited':
                print(f'Shall not have a {requ.system} reference of {requ.value}')
            
        else:
            if requ.get_usage() == 'required':
                print(f'Shall be classified using {requ.system}')

            elif requ.get_usage() == 'prohibited':
                print(f'Shall not be classified using {requ.system}')


    elif requ.__class__.__name__ == "Parts":
        print(' Requirement is at Facet Parts, showing Requirements is in procress')


    elif requ.__class__.__name__ == "Material":
        print(' Requirement is at Facet Material, showing Requirements is in procress')

    print()

##############################################################################

# IsIDScheckingPath = "C:\\temp\\revit\\IsIDSChecking.json"
dbPath = "C:\\temp\\revit\\db.json"
ConfigPath = "C:\\Users\\Sascha Hostettler\\Documents\\GitHub\\pyRevit-IDS_bSDD\\Revit-IA_Integration\\Panel.extension\\lib\\config.json"
# with open(IsIDScheckingPath) as IsIDSchecking:
#     isChecking = json.load(IsIDSchecking)

with open(ConfigPath) as ConfigFile:
    config = json.load(ConfigFile)

elementId = uidoc.Selection.GetElementIds()[0].Value

element = doc.GetElement(ElementId(elementId))
ElementTypeId = element.GetTypeId()
elementType = doc.GetElement(ElementTypeId)
cat = element.Category.Name
##############################################################################
class Classification():
    def __init__(self, ClassValue):
        self.ClassValue = ClassValue
        self.parseInput()

    def parseInput(self):

        parts = self.ClassValue.strip('[]').split(':')
        self.Class = parts[0].split(']')[0]

        if len(parts[0].split(']')) > 1:
            self.Code = parts[0].split(']')[1]

            if len(parts) > 1:
                self.Title = parts[1]
            else:
                self.Title = None
        else:
            self.Code = None
            self.Title = None

class   ClassificationHandler:
    def __init__(self, doc, RevitElement, SelectedDictionary, SelectedClass):
        self.RevitElement = RevitElement
        self.SelectedDictionary = SelectedDictionary
        self.SelectedClass = SelectedClass
        self.parameterName = None
        self.parameterValue = None
        self.doc = doc
        self.setParamter() 

    def setParamter(self):
        # try:
        getbSDDRequest(self.doc, self.RevitElement, self.SelectedDictionary, self.SelectedClass)
        # except:
            # print(f'Error occurs while bSDD request, Selected_Dictionary: {self.SelectedDictionary}, Selected_Class: {self.SelectedClass}')



with open(dbPath) as file:
    dbDataFrame = json.load(file)

for IDSName in getImportedIDS():
    print(str('\n### ') + str(IDSName) + ' ###')
    idsxml = f'C:\\temp\\revit\\{IDSName}.xml'
    my_ids = ifctester.open(idsxml)
    print(my_ids.info['title']) 

    #Ist die Category teil der Anforderung
    for Entity in dbDataFrame[IDSName]['IfcMapping']:
        if str(cat) in dbDataFrame[IDSName]['IfcMapping'][Entity] or (elementType != None and Entity.encode('utf-8') == str(elementType.LookupParameter('Export Type to IFC As').AsString()).upper().encode('utf-8')):
        # if str(Entity).encode('utf-8') == str(elementType.LookupParameter('Export Type to IFC As').AsString()).upper().encode('utf-8'):
            #Specifications
            for specification in my_ids.specifications:
                
                #Applicability 
                for appli in specification.applicability:
                    
                    if appli.__class__.__name__ == 'Entity':   

                        appliName = appli.name   
                            
                        if (str(appliName).upper() in dbDataFrame[IDSName]['IfcMapping'] and str(cat) in dbDataFrame[IDSName]['IfcMapping'][str(appliName).upper()]) or str(appliName).upper().encode('utf-8') == str(Entity).upper().encode('utf-8'):

                            print('\n')
                            print(20*'-')
                            print(specification.name)
                            print(f'The specification is {specification.get_usage()}')

                            for requ in specification.requirements:
                                getRequirements(requ, appli.name)
                                    
                            
                    elif appli.__class__.__name__ == 'Attribute':
                        for parameter in element.Parameters:
                            
                            if parameter.Definition.Name == appli.name:
                                
                                print('\n')
                                print(20*'-')
                                print(specification.name)
                                print(f'The specification is {specification.get_usage()}')

                                for requ in specification.requirements:
                                    getRequirements(requ, appli.name)       

                    elif appli.__class__.__name__ == 'Property':
                        for parameter in element.Parameters:
                            
                            if parameter.Definition.Name == appli.name:
                                
                                print('\n')
                                print(20*'-')
                                print(specification.name)
                                print(f'The specification is {specification.get_usage()}')

                                for requ in specification.requirements:
                                    getRequirements(requ, appli.name) 
                        
                    elif appli.__class__.__name__ == 'Classification':
                    
                        for parameter in element.Parameters:
                            
                            if parameter.Definition.Name == 'Classification.Space.Number':
                                
                                print('\n')
                                print(20*'-')
                                print(specification.name)
                                print(f'The specification is {specification.get_usage()}')

                                for requ in specification.requirements:
                                    getRequirements(requ, appli.system)
                    

                    elif appli.__class__.__name__ == 'Parts':
                        print('Applicability is at Facet Parts, Checking is in procress')        
                    
                    elif appli.__class__.__name__ == 'Material':
                        print('Applicability is at Facet Material, Checking is in procress')  
            print('\n')
            break
        else:
            print(f'Entity: {Entity} ist nicht Teil der geladenen Informationsanforderung')    


    print(20*'-')

    ## neu in getbSDDClass
    
    # for parameter in element.Parameters:
    #     # print(parameter)
    #     if str(parameter.Definition.Name).startswith('ClassificationCode'):
    #         ParameterValue = parameter.AsString()
    #         RevitSourceParamter = parameter.Definition.Name
    #         if ParameterValue != None and len(ParameterValue) > 1:

    #             print(10*'-')
    #             print(parameter.Definition.Name, ParameterValue)

    #             ClassValue = Classification(ParameterValue)
    #             SelectedDictionary = ClassValue.Class
    #             SelectedClass = ClassValue.Code

    #             print(SelectedDictionary, SelectedClass)

    #             # try:
    #                 # getbSDDRequest(SelectedDictionary, SelectedClass)
    #             ClassificationHandler(doc, element, ClassValue.Class, ClassValue.Code)
    #             # except:
    #                 # print(f'Error occurs while bSDD request, Selected_Dictionary: {SelectedDictionary}, Selected_Class: {SelectedClass}')
    
    # print(print(10*'-'))
    # print('\n## Ende ##')