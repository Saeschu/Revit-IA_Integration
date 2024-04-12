#! python3

### SATART of CODE ImportIDS ###
# Autor: Sascha Hostettler
# Datum: 20.05.2024
# Version: ?
# Beschrieb: 
# Effektive Funktion zum Validieren der Eingaben gegen die geladenen Informationsanforderungen.
#
### SATART of CODE ImportIDS ###
# print('\n### SATART of CODE ImportIDS ###')
##############################################################################
import ifcopenshell
import ifctester
import re
import json
import sys
import sys
import csv
import os 

from pyrevit import EXEC_PARAMS, DB
from Autodesk.Revit.DB import *
import System
from System import Enum

# sys.path.append( '/Pnale.extenstion/lib')
# from mymodule import get_RevitElementFromIFCmapping 

##############################################################################

# ConfigPath = "C:\\temp\\revit\\IsIDSChecking.json" # Alt
ConfigPath = "C:\\Users\\Sascha Hostettler\\Documents\\GitHub\\pyRevit-IDS_bSDD\\Revit-IA_Integration\\Panel.extension\\lib\\config.json"

dbPath = 'C:\\temp\\revit\\db.json'

with open(ConfigPath) as ConfigFile:
    config = json.load(ConfigFile)

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


def getRevitParameterMappingDataFrame(IDSName):
    IDSPropertySetDefinedFolderPath = "C:\\ProgramData\\Autodesk\\ApplicationPlugins\\IFC 2021.bundle\\Contents\\2021"
    IDSPropertySetDefinedFileName = str('IDSPropertySetDefined_') + str(IDSName)
    RevitParameterMappingDataFrame = list( csv.reader(open(str(IDSPropertySetDefinedFolderPath) + str('\\') + str(IDSPropertySetDefinedFileName) + str('.txt'), 'r'), delimiter='\t')  )

    return RevitParameterMappingDataFrame

def getImportedIDS():
    directory = 'C:\\temp\\revit'
    ImportedIDS = []
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            if str(filename).endswith('.xml'):
                ImportedIDS.append(filename.split('.')[0])

    return ImportedIDS 

def getIfcPropertyName(RevitParameterName, RevitParameterMappingDataFrame):

    for line in RevitParameterMappingDataFrame:
        if len(line) > 1:
            IfcName = line[1]
            RevitName = line[3]

            if RevitName != '' and RevitName == RevitParameterName:
                # print('getIfcPropertyName ', RevitParameterName, ' -> ', MappedIfcPropertyName)
                return IfcName    
            
            elif RevitName == '' and IfcName == RevitParameterName:
                # print('getIfcPropertyName ', RevitParameterName, ' -> ', MappedIfcPropertyName)
                return IfcName

def getRevitParameterName(IfcPropertyName, RevitParameterMappingDataFrame):

    for line in RevitParameterMappingDataFrame:
        if len(line) > 1:
            IfcName = line[1]
            RevitName = line[3]

            if IfcName == IfcPropertyName and RevitName != '':
                # print('getRevitParameterName ', IfcPropertyName, ' -> ',  IfcName)
                return RevitName
            
            elif IfcName == IfcPropertyName and RevitName == '':
                # print('getRevitParameterName ', IfcPropertyName, ' -> ', IfcName)
                return IfcName   

#Check Requirements
def checkRequirementValue(requ, ParameterName, ParameterValue):

    if requ.value != None and ParameterValue != None:

        if type(requ.value) == str:
            if requ.value == ParameterValue: 
                pass
            else:
                print(f'WARNING : {ParameterName}  :  "{ParameterValue}"  nicht erlaubter wert')
                print(f'Erlaubter Wertebereich : "{requ.value}"')

        elif 'pattern' in requ.value.options:
            pattern = requ.value.options['pattern']
            if re.match(pattern, ParameterValue):
                pass
            else:
                print(f'WARNING :  {ParameterName}  :  "{ParameterValue}"   nicht erlaubter Werteausdruck')
                print(f'Erlaubter Wertebereich : "{requ.value}"')

        elif 'enumeration' in requ.value.options:
            ValueList = requ.value.options['enumeration']
            if ParameterValue in ValueList:
                pass
            else:
                print(f'WARNING :  {ParameterName}  :  "{ParameterValue}"   nicht erlaubter Listenwert')
                print(f'Erlaubte Werteliste : {ValueList}')
    
    #Handeling Spezialfall wenn Wert nicht "" sondern None also nicht str ist. 
    elif requ.value != None and ParameterValue == None:
        print(f'WARNING : {ParameterName}  :  darf nicht lehr sein')
        print(f'Geforderter Wertebereich : "{requ.value}"')

    else:
        pass


#Requirements Facet
def checkRequirements(RevitElement, requ):

        ## ToDo: Attribut von reinem SingelValue auf Wertebreich umbauen.

    if requ.__class__.__name__ == "Entity":

        ## ToDo: Ausbauen um ueber Mappingfile gemappte Kategorien zu pruefen.
        ## ToDo: Einbauen preufung gege geforderte abstrakte Entitaeten
        
        try:
            RevitParameter = RevitElement.LookupParameter(f'Export to IFC As')
            RevitParameterName = f'Export to IFC As' #Revit_parameter.Name
            Revit_parameterValue = RevitParameter.AsValueString()
            try:
                RevitParameter = RevitElement.LookupParameter(f'Export Type to IFC As')
                RevitParameterName = f'Export Type to IFC As' #Revit_parameter.Name
                Revit_parameterValue = RevitParameter.AsValueString()
            except:
                print(f'Geforderter Parameter "Ifc Predefined Type" ist auf dem Typ nicht vorhanden')
                Revit_parameterValue = None
        except:
            print(f'Geforderter Parameter "Ifc Predefined Type" ist auf dem Element nicht vorhanden')
            Revit_parameterValue = None

        if Revit_parameterValue != None:
            if requ.get_usage() != 'prohibited':
                checkRequirementValue(requ, RevitParameterName, Revit_parameterValue)
            else:
                print(f'WARNING : {RevitParameterName} : Parameterwert darf nicht vorhanden sein')

        elif requ.get_usage() == 'required':
            print(f'WARNING : {RevitParameterName} : Parameterwert muss vorhanden sein')

        if requ.predefinedType != None:
            
            try:
                RevitParameter = RevitElement.LookupParameter(f'Ifc Predefined Type')
                RevitParameterName = f'Ifc Predefined Type' #Revit_parameter.Name
                Revit_parameterValue = RevitParameter.AsValueString()
            except:
                print(f'Geforderter Parameter "Ifc Predefined Type" ist nicht vorhanden')
                Revit_parameterValue = None

            if Revit_parameterValue != None:
                if requ.get_usage() != 'prohibited':
                    checkRequirementValue(requ, RevitParameterName, Revit_parameterValue)
                else:
                    print(f'WARNING : {RevitParameterName} : Parameterwert darf nicht vorhanden sein')

            elif requ.get_usage() == 'required':
                print(f'WARNING : {RevitParameterName} : Parameterwert muss vorhanden sein')

    elif requ.__class__.__name__ == "Attribute":
        
        try:
            RevitParameter = RevitElement.LookupParameter(f'Ifc{requ.name}')
            RevitParameterName = f'Ifc{requ.name}' #Revit_parameter.Name
            Revit_parameterValue = RevitParameter.AsValueString()
        except:
            print(f'Geforderter Parameter "{requ.name}" ist nicht vorhanden')
            Revit_parameterValue = None
            # forSetUpnewParamter(Revit_parameterName, 'Rooms')

        if Revit_parameterValue != None:
            if requ.get_usage() != 'prohibited':
                checkRequirementValue(requ, RevitParameterName, Revit_parameterValue)
            else:
                print(f'WARNING : {RevitParameterName} : Parameterwert darf nicht vorhanden sein')

        elif requ.get_usage() == 'required':
            print(f'WARNING : {RevitParameterName} : Parameterwert muss vorhanden sein')
    

    elif requ.__class__.__name__ == "Property":
        try:
            RevitParameterName = getRevitParameterName(requ.name, RevitParameterMappingDataFrame)          
            RevitParameter = RevitElement.LookupParameter(RevitParameterName)
            Revit_parameterValue = RevitParameter.AsValueString()
        except:
            print(f'Gefordertes Parameter "{RevitParameterName}" ist nicht vorhanden')
            RevitParameterName = None
        

        if RevitParameterName != None:
            if requ.get_usage() != 'prohibited':

                ## ToDo: Check nur auf Datentyp

                checkRequirementValue(requ, RevitParameterName, Revit_parameterValue)
            else:
                print(f'WARNING : {RevitParameterName} : Parameterwert darf nicht vorhanden sein')

        elif requ.get_usage() == 'required':
            print(f'WARNING : {RevitParameterName} : Parameterwert muss vorhanden sein')


    elif requ.__class__.__name__ == "Classification":
        AllClassSystems = []
        for parameter in RevitElement.Parameters:
        # print(parameter)
            if str(parameter.Definition.Name).startswith('ClassificationCode'):
                ParameterValue = parameter.AsString()
                if ParameterValue != None and len(ParameterValue) > 1:
                    
                    ClassValue = Classification(ParameterValue)
                    AllClassSystems.append(ClassValue.Class)

                    if ClassValue.Class == requ.system:
                        if ClassValue.Code != None:

                            checkRequirementValue(requ, ClassValue.Class,  ClassValue.Code)

                        else:
                            print(f'WARNING : {requ.system} : Code muss vorhanden sein')

        if requ.minOccurs == 1 and requ.system not in AllClassSystems:
            print(f'Gefordertes Klassifikationssystem "{requ.system}" ist nicht vorhanden') 

       
    elif requ.__class__.__name__ == "Parts":

        ## ToDo: Filtern aller Elemente der RequEntity (ueberfuert auf Revit-Kategorie) und durchsuchen der DependetElements auf aktuelles Element
        ## ToDo: Ueberfuehren der Relatio auf die Dependet von Revit

        requRelation = requ.relation 
        requEntity = requ.name

        if requEntity != None:
            if requEntity == "IfcBuildingStorey" and doc.GetElement(RevitElement.LevelId) == None:
                    print(f'WARNING :  Categeory muss vorhanden Teil von einer Ebene sein')
            
            else:              
                print(RevitElement.GetDependentElements)
                # for element in RevitElement.GetDependentElements():
                    # print(GetCategory(doc, element.Id))
                
        if requRelation != None:

            if requRelation == "IFCRELAGGREGATES":
                if doc.GetElement(RevitElement.LevelId) == None:
                    f'WARNING :  Categeory muss Teil von einer Ebene sein'

            elif requRelation == "IFCRELASSIGNSTOGROUP":
                print(f'Pruefung PartOf mit Relation: "{requRelation}" ist noch in arbeit')

            elif requRelation == "IFCRELCONTAINEDINSPATIALSTRUCTURE":
                print(f'Pruefung PartOf mit Relation: "{requRelation}" ist noch in arbeit')

            elif requRelation == "IFCRELNESTS":
                print(f'Pruefung PartOf mit Relation: "{requRelation}" ist noch in arbeit')

            elif requRelation == "IFCRELVOIDSELEMENT":
                print(f'Pruefung PartOf mit Relation: "{requRelation}" ist noch in arbeit')

            elif requRelation == "IFCRELFILLSELEMENT":
                print(f'Pruefung PartOf mit Relation: "{requRelation}" ist noch in arbeit')

            else:
                print(f'{requRelation} ist keien gueltige Relation')

        else:
            print('Invalide Anfordrderung mit PartOf')


    elif requ.__class__.__name__ == "Material":
                print(' Requirement is at Facet Material, Checking is in procress')


def chekingParameters(specification):
    print('\n')
    print(20*'-')
    print(specification.name)
    print(f'The specification is {specification.get_usage()}')

    for requ in specification.requirements:
        print(10*'-')
        try:
            checkRequirements(RevitElement, requ)
        except:
            print(f'Gefordertes Attribut "{requ.name}" ist nicht vorhanden')


def forSetUpnewParamter(Parameter, BuiltInCategory):
    print('forSetUpnewParamter')
    dbDataFrame['IDSArg']
    ParamterList = dbDataFrame['IDSArg']['NewParamter']
    ParamterList.append(Parameter)

    dbDataFrame["IfcCategoryMapping"].update({'NewParamter' : BuiltInCategory})

    file = open(dbPath, "w")
    jsonString = json.dumps(dbDataFrame)

    file.write(jsonString)
    file.close()



def IrChecking(idsXml, IfcEntity, RevitElement):
    MyIds = ifctester.open(idsXml)
                                    
    # Specifications
    for specification in MyIds.specifications:
        
        # Applicability 
        for appli in specification.applicability:
            ## ToDo Bedingung für Kardinalität applicabilty definieren
            ## ToDo Regel einbauen, dass mehrer Appli kombiniert als Schnittmenge gelten, nur Prüfen wenn alle appli erfüllt sind

            #print(appli.get_usage())
            #print(len(appli))
            
            if appli.__class__.__name__ == 'Entity':

                    ## ToDo: Preufen ob PredefinedType gesetzt ist, wenn ja zuerst pruefen ob Element diesen PredefinedType aufweist. 

                    appliName = appli.name

                    if str(appliName).upper() == str(IfcEntity).upper():
                        print(f'{str(appliName).upper()} = {str(IfcEntity).upper()}')

                        for requ in specification.requirements:
                            print(10*'-')
                            checkRequirements(RevitElement, requ)


            elif appli.__class__.__name__ == 'Attribute':

                ## ToDo: Preufen ob Attribut Value gesetzt ist, wenn ja zuerst pruefen ob Element bei diesem Parameter diesen Value aufweist. 

                for parameter in RevitElement.Parameters:

                    if str(parameter.Definition.Name).upper() == str(f'Ifc{appli.name}').upper():
                        
                        chekingParameters(specification)        


            elif appli.__class__.__name__ == 'Property':

                ## ToDo: Preufen ob Property Value gesetzt ist, wenn ja zuerst pruefen ob Element bei diesem Parameter diesen Value aufweist. 

                for parameter in RevitElement.Parameters:
                        
                    if str(getIfcPropertyName(parameter.Definition.Name, RevitParameterMappingDataFrame)).upper() == str(appli.name).upper:
                        
                        chekingParameters(specification)
                

            elif appli.__class__.__name__ == 'Classification':

                ## ToDo: Preufen ob Classification Value gesetzt ist, wenn ja zuerst pruefen ob Element bei diesem Parameter (Classification) diesen Value aufweist. 

                for parameter in RevitElement.Parameters:

                    if str(parameter.Definition.Name).startswith('Classification'):
                        
                        chekingParameters(specification)


            elif appli.__class__.__name__ == 'Parts':

                ## ToDo: Preufen ob Parts Relation gesetzt ist, wenn ja zuerst pruefen ob Element diese Relation aufweist. 

                for dependetElement in RevitElement.GetDependentElements():
                    checkRequirements(dependetElement, requ)
        
            
            elif appli.__class__.__name__ == 'Material':
                # GetMaterialIds (Boolean): ICollection<ElementId>
                print('Applicability is at Facet Material, Checking is in procress')  

    # print(f'Applicability  {appli.name} - Requirement {requ.__class__.__name__}, {requ.name} : {requ.value} , {type(requ.value)}')

##############################################################################
## __MAIN__ ##

# Validierung wird bei jeder Aenderung der Autodesk.DB getrigger, daher durchlaufen Code nur, wenn IsIDSChecking aktiviert.
if config['IsIDSChecking'] == True:

    if len(EXEC_PARAMS.event_args.GetModifiedElementIds()) > 0 and config['IsIDSChecking'] == True:
        print(20*'-')
        print(EXEC_PARAMS.event_args.GetTransactionNames()) 
      
        # Oeffnen der db
        with open(dbPath) as file:
            dbDataFrame = json.load(file)

        # Validierung durchlaufen fuer jedes importierte IDS
        for IDSName in getImportedIDS():
            if IDSName in dbDataFrame:
                print(str('\n### ') + str(IDSName) + ' ###')
                idsXml = f'C:\\temp\\revit\\{IDSName}.xml' 
                RevitParameterMappingDataFrame = getRevitParameterMappingDataFrame(IDSName)

                # Validierung aller geaenderte Elementen 
                for elementId in EXEC_PARAMS.event_args.GetModifiedElementIds():

                    doc = EXEC_PARAMS.event_args.GetDocument()
                    cat = None           
                    RevitElement = doc.GetElement(elementId)

                    # Unterscheiden ob Instanz oder Typ geaendert wurde
                    if EXEC_PARAMS.event_args.GetTransactionNames()[0] == 'Modify element attributes':
                        cat = RevitElement.Category.Name

                        # Unoetiges durchlaufend von Elementen vermeiden
                        if cat != None and cat != 'Schedules':
                            print(30*'-')
                            print(str('## element.Category.Name: "') + str(cat) + str('" get validated'))
                            print(30*'-')
                    
                            
                            # Ist die Category des geanderten Element Teil der Anforderung
                            for IfcEntity in dbDataFrame[IDSName]['IfcMapping']:
                                if str(cat) in dbDataFrame[IDSName]['IfcMapping'][IfcEntity]:

                                    print(f'## IfcMapping of Entity: {IfcEntity}')
                                    print(dbDataFrame[IDSName]['IfcMapping'][IfcEntity])
                                    print('##')

                                    # Validierung aller Parameter, des geaenderten Elementes gegen das IDS
                                    IrChecking(idsXml, IfcEntity, RevitElement)
                 
                    elif EXEC_PARAMS.event_args.GetTransactionNames()[0] == 'Modify type attributes':

                        try:
                            if RevitElement.FamilyName != None:
                               
                                IfcEntity = RevitElement.LookupParameter('Export Type to IFC As').AsString()
                                print(f'## IfcMapping of Type Entity: {IfcEntity}')
                                print(f'## Revit Element of Type : {RevitElement}')
                                print('##')

                                # Validierung aller Parameter, des geaenderten Types gegen das IDS
                                IrChecking(idsXml, IfcEntity, RevitElement)

                        except:
                            'ist keine Familie'

            else:
                'Info 348'

        print(10*'-') 
        print(20*'-') 