#! python3
### SATART of CODE getbSDDClass ###
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
from lib.bSDDRequest import getbSDDRequest, get_dictionaries, get_classes, get_classInof, get_classProperties
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
    def __init__(self, SelectedDictionary, SelectedClass):
        self.SelectedDictionary = SelectedDictionary
        self.SelectedClass = SelectedClass
        self.parameterName = None
        self.parameterValue = None
        
        print(f'{self.SelectedDictionary} = {self.SelectedClass}')

        if type(self.SelectedClass) == str:
            self.ClassPropertyList = getbSDDRequest(str(self.SelectedDictionary), str(self.SelectedClass))

        elif  'enumeration' in self.SelectedClass.options:
            for requClass in requ.value.options['enumeration']:
                self.ClassPropertyList = getbSDDRequest(self.SelectedDictionary, requClass)
        
        elif  'pattern' in self.SelectedClass.options:
            print('bSDD suche mitt Pattern noch nicht unterstuetzt')

        

    def setClassPredefinedPropertyValue(self, doc, RevitElement, RevitSourceParamter):
        RevitTargetParamterCode = str(RevitSourceParamter)
        RevitTargetParamterDescription = str(f'{RevitSourceParamter} Description')  
        
        RevitParamterCode = RevitElement.LookupParameter(RevitTargetParamterCode)     
        RevitParamterDescription = RevitElement.LookupParameter(RevitTargetParamterDescription)
        
        
        
        t = Transaction(doc, "Ergaenze Classification Parameter")
        t.Start()
        # classProperty["predefinedValue"])
        
        RevitParamterCode.Set(str(f'[{self.SelectedDictionary}]{self.SelectedClass}'))
        RevitParamterDescription.Set(str(self.ClassPropertyList).strip('[]'))
        
        
        t.Commit()


def getImportedIDS():
    directory = 'C:\\temp\\revit'
    ImportedIDS = []
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            if str(filename).endswith('.xml'):
                ImportedIDS.append(filename.split('.')[0])

    return ImportedIDS 

#Check Requirements
def getRequirements(requ, appliName):

    if requ.__class__.__name__ == "Classification":
        # Klassifikatinen werden anhand der Informationsanforderung mit Klassifikationssystem und code gesucht und aufgelistet
        if requ.value != None:                                            
            if requ.get_usage() == 'required':
                print(f'Shall have a {requ.system} reference of {requ.value}')
                print('Moegliche selektionen bSDD: System und Class')
                
                ClassificationHandler(requ.system, requ.value)

                SelectedClass = input('\nEingabe der Klassifikation welche in Revit uebernommen werden soll: [Korridor]').strip('\x00')
                for parameter in element.Parameters:
                    if str(parameter.Definition.Name).startswith('ClassificationCode') and str(parameter.Definition.Name).endswith('Description') == False:
                        ParameterValue = parameter.AsString()
                        if ParameterValue == None or len(ParameterValue) < 1:
                            RevitSourceParamter = parameter.Definition.Name
                            
                            ClassificationHandler(requ.system, SelectedClass).setClassPredefinedPropertyValue( doc, element, RevitSourceParamter)
                            break

                return requ.system, requ.value
                
            elif requ.get_usage() == 'prohibited':
                print(f'Shall not have a {requ.system} reference of {requ.value}')
                return None, None
            
        else:
            # Klassifikatinen werden anhand der Informationsanforderung mit Klassifikationssystem und der assoziation der klassifikation auf bsdd aufgelistet
            if requ.get_usage() == 'required':
                print(f'Shall be classified using {requ.system}')
                print('Moegliche selektionen : System')
                dictionaries = get_dictionaries()

                for dictionary in dictionaries['dictionaries']:
                    if dictionary['name'] == requ.system:
                        ParentClass = {}
                        for classItem in dictionary["classes"]:
                            if classItem['classType'] =='Class':
                                Class = get_classInof(classItem["uri"])
                                if Class != None and 'parentClassReference' not in Class and appliName in Class['relatedIfcEntityNames']:
                                    
                                    # ToDo: Falls ClassPropert != None: Abfragen aller Propoerties der Klassifikation und vergelich mit gemappten Paramter in Revit, falls Wert = Wert ClassParamter ist Klassifikation zugelassen.
                                    
                                    print(f'- {Class["name"]}')
                                    ParentClass[Class['name']] = Class['uri']

                SelectedClass = input('Eingabe Klassifikation: [Korridor]').strip('\x00')
                browsBsddClasses(True, ParentClass, SelectedClass )

                return requ.system, None

            elif requ.get_usage() == 'prohibited':
                print(f'Shall not be classified using {requ.system}')
                return None, None
            
    else:
        return 'No Classification'

    print()


def browsBsddClasses(getParentClass, ParentClass, SelectedClass ):

    while getParentClass ==  True:
        
        Class = get_classInof(ParentClass[SelectedClass])
        
        if 'childClassReferences' in Class:

            for ChildClass in Class['childClassReferences']:
                ClassInfo = get_classProperties(ChildClass["uri"])[0]
                ParentClass[ClassInfo['name']] = ClassInfo['uri']


            SelectedClass = input("\nSelect an ParentClass: ").strip('\x00')
            # SelectedClass = "RoomType"
            print(f"Selected_ParentClass = '{SelectedClass}'")

        else:
            getParentClass = False
            print(f"{SelectedClass} has no child Classes")
                    
            if 'classProperties' in Class:
                get_classProperties(Class["uri"])

            
            updateRevit = input('soll die angegebene Klassifikation dem selektierten Element zugewiesen werden: [Ja/Nein]').strip('\x00')
            
            if updateRevit == "Ja":
                
                for parameter in element.Parameters:
                    print(f'{parameter.Definition.Name} = {parameter.AsString()}')
                    if str(parameter.Definition.Name).startswith('ClassificationCode') and str(parameter.Definition.Name).endswith('Description') == False:
                        ParameterValue = parameter.AsString()
                        if ParameterValue == None or len(ParameterValue) < 1:
                            RevitSourceParamter = parameter.Definition.Name
                            
                            ClassificationHandler(SelectedDictionary.strip(f' {SelectedDictionary.split(" ")[-1]}'), SelectedClass).setClassPredefinedPropertyValue( doc, element, RevitSourceParamter)
                            
                            break
            else:
                print(updateRevit)
                break


##############################################################################


dbPath = "C:\\temp\\revit\\db.json"
ConfigPath = "C:\\Users\\Sascha Hostettler\\Documents\\GitHub\\pyRevit-IDS_bSDD\\Revit-IA_Integration\\Panel.extension\\lib\\config.json"
browsBsddisTrue = True

with open(ConfigPath) as ConfigFile:
    config = json.load(ConfigFile)

with open(dbPath) as file:
    dbDataFrame = json.load(file)

elementId = uidoc.Selection.GetElementIds()[0].Value

element = doc.GetElement(ElementId(elementId))
ElementTypeId = element.GetTypeId()
elementType = doc.GetElement(ElementTypeId)
cat = element.Category.Name
##############################################################################
##__MAIN__##

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

                            for requ in specification.requirements:
                                myRequClass = getRequirements(requ, appli.name)

                            
                    elif appli.__class__.__name__ == 'Attribute':
                        for parameter in element.Parameters:
                            
                            if parameter.Definition.Name == appli.name:

                                for requ in specification.requirements:
                                    myRequClass = getRequirements(requ, appli.name)       

                    elif appli.__class__.__name__ == 'Property':
                        for parameter in element.Parameters:
                            
                            if parameter.Definition.Name == appli.name:

                                for requ in specification.requirements:
                                    myRequClass = getRequirements(requ, appli.name) 
                        
                    elif appli.__class__.__name__ == 'Classification':
                    
                        for parameter in element.Parameters:
                            
                            if parameter.Definition.Name == 'Classification.Space.Number':

                                for requ in specification.requirements:
                                    myRequClass = getRequirements(requ, appli.system)
                    
            print('\n')
            break
        else:
            print(f'Entity: {Entity} ist nicht Teil der geladenen Informationsanforderung')    

    print(20*'-')


browsBsdd = "nein"

if browsBsddisTrue == True:
    print(print(10*'-'))
    print('\n## Brows bSDD ##')
    browsBsdd = input('Wollen Sie das bSDD manuell durchsuchen: [Ja/Nein]').strip('\x00')
           
if browsBsdd == "Ja":

    ##############################################################################################
    #Wenn keine Klassifikation gefordert ist kann das bSDD regulaer durchsucht werden
    dictionaries = get_dictionaries()

    tempDictionaries = {}
    for dictionary in dictionaries['dictionaries']:
        tempDictionaries[str(dictionary['name'] + " " + dictionary['version'])] = dictionary['uri']
        print('Dictionary Name: ', str(dictionary['name'] + " " + dictionary['version']))

    ##############################################################################################
    #Wenn keine Klassifikation gefordert ist kann das bSDD regulaer durchsucht werden
    SelectedDictionary = input(" Eingabe Dictionary ['FM waveware Spital'] ")
    # if len(SelectedDictionary) == 0:
    SelectedDictionary = "FM waveware Spital 2.0"
    # Selected_Domain = "FM waveware Spital"
    print(f"Selected_Domain = '{SelectedDictionary}'")
        ##############################################################################################
    domain_namespaceUri = tempDictionaries[SelectedDictionary]


    #Clases of the Domain
    if dictionaries:
        # domain_namespaceUri = 'https://identifier.buildingsmart.org/uri/bs-agri/fruitvegs/1.0.0' #Eingabe erfolgt über wahl der Domain Name => Domain Uri
        dictionary = get_classes(domain_namespaceUri)["dictionary"]
        ClassList= []

        ParentClass = {}

        #Get PartenClasses
        for classItem in dictionary["classes"]:
            # for classItem in classes["classes"]:
            if classItem['classType'] =='Class':
                Class = get_classInof(classItem["uri"])
                    
                if Class != None and 'parentClassReference' not in Class:
                    print(f'- {Class["name"]}')
                    ParentClass[Class['name']] = Class['uri']
                    getParentClass = True

    ##############################################################################################
    SelectedClass = input("Eingabe PartentClass ['RoomCommon'] ")
    # if len(SelectedClass) == 0:
    SelectedClass = "RoomCommon"
        # Selected_ParentClass = "RoomCommon"
    print(f"Selected_ParentClass = '{SelectedClass}'")
    ##############################################################################################

    browsBsddClasses(getParentClass, ParentClass, SelectedClass)

else:
    print(browsBsdd)
    

print("\nEnde of Code")
