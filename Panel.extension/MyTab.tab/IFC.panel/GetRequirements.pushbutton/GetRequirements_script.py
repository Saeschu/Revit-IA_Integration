#! python3

#############################################################################
import json
from bSDDRequest import getbSDDRequest
import ifctester

from pyrevit import EXEC_PARAMS, DB
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
import System
from System import Enum

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application

##############################################################################


#####
  

#Check Requirements
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
                print(f'{requ.name} data shall be {requ.alue} and in the dataset {requ.propertySet}')

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


IsIDScheckingPath = "C:\\temp\\revit\\IsIDSChecking.json"
idsxml = "C:\\temp\\revit\\ids.xml"
dbPath = "C:\\temp\\revit\\db.json"

with open(IsIDScheckingPath) as IsIDSchecking:
    isChecking = json.load(IsIDSchecking)


elementId = uidoc.Selection.GetElementIds()[0].Value

element = doc.GetElement(ElementId(elementId))
cat = element.Category.Name
##############################################################################

with open(dbPath) as file:
    db = json.load(file)


#Ist die Category teil der Anforderung
for Entity in db['IfcCategoryMapping']:
    if str(cat).upper() in db['IfcCategoryMapping'][Entity]:

        my_ids = ifctester.open(idsxml)
        print(my_ids.info['title']) 

        #Specifications
        for specification in my_ids.specifications:
            
            #Applicability 
            for appli in specification.applicability:
                
                if appli.__class__.__name__ == 'Entity':   

                    appliName = appli.name   
                        
                    if str(appliName).upper() in db['IfcCategoryMapping'] and str(cat) in db['IfcCategoryMapping'][str(appliName).upper()]:

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
        print('Entity ist nicht Teil der geladenen Informationsanforderung')    


print(20*'-')
for parameter in element.Parameters:
    # print(parameter)
    if parameter.Definition.Name == 'Classification.Space.Number':
        print(10*'-')
        sp_Name = element.LookupParameter('Classification.Space.Description')
        Selected_Dictionary = sp_Name.AsString()
        Selected_Class = parameter.AsValueString()

        print(Selected_Dictionary, Selected_Class)

        try:
            getbSDDRequest(Selected_Dictionary, Selected_Class)
        except:
            print(f'Error occurs while bSDD request, Selected_Dictionary: {Selected_Dictionary}, Selected_Class: {Selected_Class}')

print('Ende')