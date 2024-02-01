#! python3
### SATART of CODE ImportIDS ###
print('\n### SATART of CODE ImportIDS ###')
##############################################################################
# import ifcopenshell
import ifctester
import re
import json

from pyrevit import EXEC_PARAMS, DB
from Autodesk.Revit.DB import *
import System
from System import Enum
##############################################################################
### Variables

IsIDScheckingPath = "C:\\temp\\revit\\IsIDSChecking.json"
idsxml = "C:\\temp\\revit\\ids.xml"
dbPath = "C:\\temp\\revit\\db.json"

with open(IsIDScheckingPath) as IsIDSchecking:
    isChecking = json.load(IsIDSchecking)

##############################################################################
          
#Check Requirements
def checkRequirements(requ, Revit_parameter, Revit_parameterValue):

    if requ.value != None:

        if type(requ.value) == str:
            if requ.value == Revit_parameterValue: 
                pass
            else:
                print(f'WARNING : {Revit_parameter}  :  {Revit_parameterValue}  nicht erlaubter wert')

        elif 'pattern' in requ.value.options:
            pattern = requ.value.options['pattern']
            if re.match(pattern, Revit_parameterValue):
                pass
            else:
                print(f'WARNING :  {Revit_parameter}  :  {Revit_parameterValue}   nicht erlaubter Werteausdruck')
                print(f'Erlaubter Wertebereich : {requ.value}')

        elif 'enumeration' in requ.value.options:
            if Revit_parameterValue in requ.value.options['enumeration']:
                pass
            else:
                print(f'WARNING :  {Revit_parameter}  :  {Revit_parameterValue}   nicht erlaubter Listenwert')
                print(f'Erlaubte Werteliste : {requ.value}')
    
    else:
        pass


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



            if isChecking['IsIDSChecking'] == True:
                #Soll live die Eingabe geprüft werden öffnen des db files => kann dies ggf. während der laufzeit in der ram vorgehlten werden?
                with open(dbPath) as file:
                    db = json.load(file)

                    
                    # print("EVENT  :", event)

                    #Ist die Category teil der Anforderung
                    for Entity in db['IfcCategoryMapping']:
                        if str(cat) in db['IfcCategoryMapping'][Entity]:

                            #ist der geänderte Paramter teil des IDS wird dies für die Prüfung geöffnet => kann dies ggf. während der laufzeit in der ram vorgehlten werden?
                            my_ids = ifctester.open(idsxml)
                            
                            #Specifications
                            for specification in my_ids.specifications:

                                #Applicability 
                                for appli in specification.applicability:
                                    
                                    if appli.__class__.__name__ == 'Entity':
                                            if appli.name == Entity:
                                                
                                        
                                                for requ in specification.requirements:
                                                    print(10*'-')
                                                    #Requirements Facet
                                                    if requ.__class__.__name__ == "Attribute" or requ.__class__.__name__ == "Property":
                                                        
                                                        # print(f'Applicability  {appli.name} - Requirement {requ.__class__.__name__}, {requ.name} : {requ.value} , {type(requ.value)}')
                                                        
                                                        Revit_parameter = element.LookupParameter(requ.name)
                                                        Revit_parameterName = requ.name #Revit_parameter.Name
                                                        Revit_parameterValue = Revit_parameter.AsValueString()

                                                        if Revit_parameterValue != None:
                                                            checkRequirements(requ, Revit_parameterName, Revit_parameterValue)
                                                        elif requ.minOccurs == 1:
                                                            print(f'WARNING : {Revit_parameterName} : Attributwerte muss vorhanden sein')

                                                    elif requ.__class__.__name__ == "Classification":
                                                        
                                                        # print(f'Applicability  {appli.name} - Requirement {requ.__class__.__name__}, {requ.system} : {requ.value} , {type(requ.value)}')
                                                        
                                                        Revit_parameter = element.LookupParameter('Classification.Space.Number')
                                                        Revit_parameterName = requ.system
                                                        Revit_parameterValue = Revit_parameter.AsValueString()
                                                        
                                                        if Revit_parameterValue != None:
                                                            checkRequirements(requ, Revit_parameterName, Revit_parameterValue)
                                                        elif requ.minOccurs == 1:
                                                            print(f'WARNING : {Revit_parameterName} : Attributwerte muss vorhanden sein')


                                                    elif requ.__class__.__name__ == "Parts":
                                                        print(' Requirement is at Facet Parts, Checking is in procress')

                                                    elif requ.__class__.__name__ == "Material":
                                                        print(' Requirement is at Facet Material, Checking is in procress')

                                            
                                    elif appli.__class__.__name__ == 'Attribute':
                                        print('Applicability is at Facet Attibute, Checking is in procress')        

                                    elif appli.__class__.__name__ == 'Property':
                                        print('Applicability is at Facet property, Checking is in procress')
                                        
                                    elif appli.__class__.__name__ == 'Classification':
                                        print('Applicability is at Facet classification, Checking is in procress')
                                
                                    elif appli.__class__.__name__ == 'Parts':
                                        print('Applicability is at Facet Parts, Checking is in procress')        
                                    
                                    elif appli.__class__.__name__ == 'Material':
                                        print('Applicability is at Facet Material, Checking is in procress')  



            
     

           


                            
            
        print(10*'-') 
        print(20*'-') 