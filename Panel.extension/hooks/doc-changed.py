#! python3
### SATART of CODE ImportIDS ###
# print('\n### SATART of CODE ImportIDS ###')
##############################################################################
# import ifcopenshell
import ifctester
import re
import json
import sys
import sys
import csv

# sys.path.append( '/Pnale.extenstion/lib')
# from mymodule import get_RevitElementFromIFCmapping

from pyrevit import EXEC_PARAMS, DB
from Autodesk.Revit.DB import *
import System
from System import Enum
##############################################################################
### Variables
IDSName = "IDS"

IsIDScheckingPath = "C:\\temp\\revit\\IsIDSChecking.json"
idsxml = "C:\\temp\\revit\\ids.xml"
dbPath = "C:\\temp\\revit\\db.json"

IDSPropertySetDefinedFolderPath = "C:\\ProgramData\\Autodesk\\ApplicationPlugins\\IFC 2021.bundle\\Contents\\2021"
IDSPropertySetDefinedFileName = str('IDSPropertySetDefined_') + str(IDSName)


with open(IsIDScheckingPath) as IsIDSchecking:
    isChecking = json.load(IsIDSchecking)


RevitParameterMappingDataFrame = list( csv.reader(open(str(IDSPropertySetDefinedFolderPath) + str('\\') + str(IDSPropertySetDefinedFileName) + str('.txt'), 'r'), delimiter='\t')  )

##############################################################################
def getIfcPropertyName(RevitParameterName, RevitParameterMappingDataFrame):

    for line in RevitParameterMappingDataFrame:
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
        IfcName = line[1]
        RevitName = line[3]

        if IfcName == IfcPropertyName and RevitName != '':
            # print('getRevitParameterName ', IfcPropertyName, ' -> ',  MappedRevitParameterName)
            return RevitName
        
        elif IfcName == IfcPropertyName and RevitName == '':
            # print('getRevitParameterName ', IfcPropertyName, ' -> ', MappedIfcPropertyName)
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
def checkRequirements(element, requ):
    if requ.__class__.__name__ == "Attribute":
        
        try:
            RevitParameter = element.LookupParameter(f'Ifc{requ.name}')
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
            RevitParameter = element.LookupParameter(RevitParameterName)
            Revit_parameterValue = RevitParameter.AsValueString()
        except:
            print(f'Gefordertes Parameter "{RevitParameterName}" ist nicht vorhanden')
            RevitParameterName = None
        

        if RevitParameterName != None:
            if requ.get_usage() != 'prohibited':
                checkRequirementValue(requ, RevitParameterName, Revit_parameterValue)
            else:
                print(f'WARNING : {RevitParameterName} : Parameterwert darf nicht vorhanden sein')

        elif requ.get_usage() == 'required':
            print(f'WARNING : {RevitParameterName} : Parameterwert muss vorhanden sein')


    elif requ.__class__.__name__ == "Classification":
        try:      
            RevitParameter = element.LookupParameter('Classification.Space.Number')
            RevitParameterName = requ.system
            Revit_parameterValue = RevitParameter.AsValueString()
        except:
            print(f'Gefordertes Parameter "Classification.Space.Number" ist nicht vorhanden')
            Revit_parameterValue = None
            # forSetUpnewParamter(Revit_parameterName, element.Category.Name)

        if Revit_parameterValue != None:
            checkRequirementValue(requ, RevitParameterName, Revit_parameterValue)
        elif requ.minOccurs == 1:
            print(f'WARNING : {RevitParameterName} : Parameterwert muss vorhanden sein')


    elif requ.__class__.__name__ == "Parts":
        print(' Requirement is at Facet Parts, Checking is in procress')


    elif requ.__class__.__name__ == "Material":
        print(' Requirement is at Facet Material, Checking is in procress')



def chekingParamters(specification):
    print('\n')
    print(20*'-')
    print(specification.name)
    print(f'The specification is {specification.get_usage()}')

    for requ in specification.requirements:
        print(10*'-')
        try:
            checkRequirements(element, requ)
        except:
            print(f'Gefordertes Attribut "{requ.name}" ist nicht vorhanden')

def forSetUpnewParamter(Parameter, BuiltInCategory):
    print('forSetUpnewParamter')
    db['IDSArg']
    ParamterList = db['IDSArg']['NewParamter']
    ParamterList.append(Parameter)

    db["IfcCategoryMapping"].update({'NewParamter' : BuiltInCategory})

    file = open(dbPath, "w")
    jsonString = json.dumps(db)

    file.write(jsonString)
    file.close()

##############################################################################
##### __MAIN__ #####

if isChecking['IsIDSChecking'] == True:


    doc = EXEC_PARAMS.event_args.GetDocument()
    my_ids = ifctester.open(idsxml)
    with open(dbPath) as file:
        db = json.load(file)



    if len(EXEC_PARAMS.event_args.GetModifiedElementIds()) > 0:
        print(20*'-')

        for elementId in EXEC_PARAMS.event_args.GetModifiedElementIds():
            
            element= doc.GetElement(elementId)
            cat = element.Category.Name
            print(30*'-')
            print('## element.Category.Name')
            print(cat)
            print('##')


            if isChecking['IsIDSChecking'] == True:
                
                print('is checking')
                print(30*'-')
                #Soll live die Eingabe geprüft werden öffnen des db files => kann dies ggf. während der laufzeit in der ram vorgehlten werden?
                with open(dbPath) as file:
                    db = json.load(file)

                    #Ist die Category teil der Anforderung
                    for Entity in db['IfcMapping']:
                        print('Entity : ', Entity)        
                        if str(cat).upper() != 'SCHEDULES' and str(cat) in db['IfcMapping'][Entity]:
                            print(f'## IfcMapping of {Entity}')
                            print(db['IfcMapping'][Entity])
                            print('##')

                            #ist der geänderte Paramter teil des IDS wird dies für die Prüfung geöffnet => kann dies ggf. während der laufzeit in der ram vorgehlten werden?
                            my_ids = ifctester.open(idsxml)
                            
                            #Specifications
                            for specification in my_ids.specifications:
                                
                                #Applicability 
                                for appli in specification.applicability:
                                    
                                    if appli.__class__.__name__ == 'Entity':

                                            appliName = appli.name

                                            if str(appliName).upper() == str(Entity).upper():
                                                print(f'{str(appliName).upper()} = {str(Entity).upper()}')
                                        
                                                for requ in specification.requirements:
                                                    print(10*'-')
                                                    checkRequirements(element, requ)


                                    elif appli.__class__.__name__ == 'Attribute':
                                        for parameter in element.Parameters:
                        
                                            if str(parameter.Definition.Name).upper() == str(f'Ifc{appli.name}').upper():
                                                
                                                chekingParamters(specification)        

                                    elif appli.__class__.__name__ == 'Property':
                                        for parameter in element.Parameters:
                        
                                            if str(parameter.Definition.Name).upper() == str(appli.name).upper:
                                                
                                                chekingParamters(specification)
                                        
                                    elif appli.__class__.__name__ == 'Classification':
                                        for parameter in element.Parameters:
                        
                                            if str(parameter.Definition.Name).upper() == str('Classification.Space.Number').upper():
                                                
                                                chekingParamters(specification)


                                    elif appli.__class__.__name__ == 'Parts':
                                        # LevelId: Ebene 0, ID24770
                                        # GetDependentElements (ElementFilter): List<ElementId>
                                        print('Applicability is at Facet Parts, Checking is in procress')        
                                    
                                    elif appli.__class__.__name__ == 'Material':
                                        # GetMaterialIds (Boolean): ICollection<ElementId>
                                        print('Applicability is at Facet Material, Checking is in procress')  

                            # print(f'Applicability  {appli.name} - Requirement {requ.__class__.__name__}, {requ.name} : {requ.value} , {type(requ.value)}')

        print(10*'-') 
        print(20*'-') 