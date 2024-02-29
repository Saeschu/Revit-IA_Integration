#! python3

##Test Pyrevit###
print('### START ###')
#############################################################################
# from pyrevit import revit, DB, forms,script, EXEC_PARAMS
# from pyrevit.forms import WPFWindow
# from Autodesk.Revit.DB import *
# import System
# from System import Enum
# import sys
# import clr
# import json
# import time

# import ifcopenshell
import ifctester
import re
import json

# from pyrevit import EXEC_PARAMS, DB
# from Autodesk.Revit.DB import *
# import System
# from System import Enum
##############################################################################

##############################################################################
# Application Members
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application
##############################################################################

# output = script.get_output()
# output.add_style('body { color: blue; }')
# ##############################################################################
### Variables



### SATART of CODE ImportIDS ###
print('\n### SATART of CODE ImportIDS ###')
##############################################################################
# Import necessary Revit API classes
# from pyrevit import revit, DB
# from pyrevit import forms,script, EXEC_PARAMS
# from pyrevit.forms import WPFWindow
from Autodesk.Revit.DB import *
import System
from System import Enum
import clr
# import clr
# import json


##############################################################################

##############################################################################
def set_new_parameter_to_Category(app, spFile,builtinCategory, paramterGroupName, parameter_name, paramter_DataType, tooltip):
  
    # Get the BindingMap of the current document
    binding_map = doc.ParameterBindings
    
    
    # Create a category set and insert the category into it
    my_categories = app.Create.NewCategorySet()

    # Use BuiltInCategory to get the category of wall  #ggf. hier ohne get Categorie da beriets eine built in Categorie uebergen wird.
    my_category = Category.GetCategory(doc, builtinCategory) 
    my_categories.Insert(my_category)

    #Check if a ParameterBindung of paramter_name already Exist
    iterator = binding_map.ForwardIterator()
    ExistParamterBindung = False
    while (iterator.MoveNext()):

        if iterator.Key.Name == parameter_name:

            CategorySet = iterator.Current.Categories
            ExistParamterBindung = CategorySet.Contains(my_category)

    print(parameter_name, ExistParamterBindung)
    
    if ExistParamterBindung == False:
        print(" Paramter will be added to Category")

    
        # Create a new group in the shared parameters file if not allready exist

        my_groups = spFile.Groups
    
        all_groups = {}
        for group in my_groups:
            all_groups[group.Name] = group


        if paramterGroupName not in all_groups:
            my_group = my_groups.Create(paramterGroupName)
            print("     Group created:  ", my_group.Name)

        else:
            my_group = all_groups[paramterGroupName]
            print("     Group alread exist: ", my_group.Name)      


        # Create an instance definition of the Parameter in definition group MyParameters

        all_paramters ={}
        for parameter in my_group.Definitions:
            all_paramters[parameter.Name] = parameter

        if parameter_name  not in all_paramters:

            option = ExternalDefinitionCreationOptions(parameter_name, paramter_DataType)
            
            # Set tooltip
            option.Description = tooltip
        
            my_definition_product_date = my_group.Definitions.Create(option)
            print("     Parameter created:  ", parameter_name)


        else:
            my_definition_product_date = all_paramters[parameter_name]
            print("     Parameter allready exist:   ", parameter_name)



        # Create an instance of InstanceBinding for the Parameter
        instance_binding = app.Create.NewInstanceBinding(my_categories)
        print("     instance_binding Created:   ", instance_binding)

    
        # Bind the definitions to the document
        instance_bind_ok = binding_map.Insert(my_definition_product_date,
                                            instance_binding, BuiltInParameterGroup.PG_IFC)
        
        print("     instance_bind_ok binded to the document:   ", instance_bind_ok)
        
        return instance_bind_ok


##############################################################################

##############################################################################
# Application Members
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application

##############################################################################
#Imput Data from IDS/Json Import
dbPath = "C:\\TEMP\\revit\\db.json"
with open(dbPath) as file:
    db = json.load(file)

# print("\n## IfcCategoryMapping")
# for i in db['IfcCategoryMapping']:
#     print(str(db['IfcCategoryMapping'][i]))
# print('##')

getBuiltInCategoryUserLabel = {}
usedBuiltInCategory = []
for cat in System.Enum.GetValues(BuiltInCategory):
    try:
        getBuiltInCategoryUserLabel[str(app.DB.LabelUtils.GetLabelFor(cat)).upper()] = cat
    except:
        pass   

# parameterlistFromIDS = ['IfcGUID', 'IfcName', 'IfcDescription','IFC Predefined Typ', 'IfcObjectType']
# parameterlistFromIDS = ["IFC Predefined Typ", "IfcName", "Neuer Parameter"]
#TEMP#
dicList = []
db['ParamArg'] ={}
####
spFile   = app.OpenSharedParameterFile()
paramterGroupName = "IR-FM_fromIDS"
paramter_DataType = SpecTypeId.String.Text
tooltip ="Tag: IDS, Description: Parameter Creadet from IDS Requirement"
####

#Main
##############################################################################

# Start Transaction:
t = Transaction(doc, "Add Parameters from IDS to Wall-elements")
t.Start()

print('## IDSArg Keys')
print(db['IDSArg'].keys())
print('##')

for entity in db['IDSArg'].keys():
    #Return: IFCSPACE, IFCSPACETYPE

    # for entity in ids['IfcCategoryMapping']:
    #     #Return: "IfcCategoryMapping": {"IFCSPACE": ["Rooms", "Rooms", "Rooms", "Rooms"]}}
        print('## IfcCategoryMapping Keys')
        print(db['IfcCategoryMapping'].keys())
        print('##')

        if str(entity).upper() in db['IfcCategoryMapping'].keys():
            print('## Entity to Creat a Parameter in')
            print(entity)

            for category in db['IfcCategoryMapping'][entity]:
                print('\n## Matching Category to Entity to Creat a Parameter in')
                print(category)

                if category in getBuiltInCategoryUserLabel:
                    builtinCategory = getBuiltInCategoryUserLabel[category]
            
                    print(str('##Setting Parameter for Category : ') + str(builtinCategory))

                    parameter_name = db['IDSArg'][entity]
                    print(parameter_name)
                    for paramter in parameter_name:
                        print('##List of Parameter', paramter)
                        try:
                            set_new_parameter_to_Category(app, spFile, builtinCategory, paramterGroupName, paramter, paramter_DataType, tooltip)
                            print('Paramter ', paramter, ' is Created')

                            parameterDic = {'ifcEntity' : str(entity),
                                            'category' : str(category),
                                            'builtinCategory' : str(builtinCategory.ToString()),
                                            'paramterGroupName' : str(paramterGroupName),
                                            'parameterName' : str(paramter),
                                            'spFileName' : str(spFile.Filename),
                                            }
                            print(parameterDic)
                            db['ParamArg'].update({str(paramter): parameterDic})

                        except:
                            pass

                else:
                    print()
# print(parameterDic)

# End Transaction:
t.Commit()

# ids["usedBuiltInCategory"] = usedBuiltInCategory
file = open(dbPath, "w")
jsonString = json.dumps(db, file)

file.write(jsonString)
file.close()

##############################################################################

### ENDE of CODE ###
print('\n### ENDE of CODE ###')












# ElementID = ElementId(179398) #IfcName: Wand 1

# element = doc.GetElement(ElementID)
# ElementParameter = element.Parameters
# print(element)
# print(ElementParameter)

# for param in ElementParameter:
#     print(param.Name)

#Get Element by Filter
# all_Rooms = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Rooms).WhereElementIsNotElementType().ToElements()


# n= 0

# while n < 3:
#     print(10*'-')


#     print(app.DocumentChanged)
#     print(doc.GetModifiedElementIds())
    
#     for Rooms in all_Rooms:
        
# #Get Shared Paramter
#         sp_Name = Rooms.LookupParameter('Name')
#         print(sp_Name.AsString())
    
    
    # print(10*'-')    
    # n = n + 1

    # time.sleep(5)






##############################################################################
print('### ENDE ###')

















#############################################################################
# print(DB.LabelUtils.GetLabelFor(BuiltInCategory.OST_Rooms))

# for cat in System.Enum.GetValues(DB.BuiltInCategory):
    # print(cat)

# print(sys.version)
# print("\n##.sys.path:")
# print('\n'.join(sys.path))

# def print_html(output_str):
#     print(output_str.replace('<', '&clt;').replace('>', '&cgt;'))
# #clr.AddReference('Autodesk.Revit.DB')
# # import Autodesk.Revit.DB as DB

# print('\n## UIApplication:')



# print(__revit__)

# # cl = DB.FilteredElementCollector(__revit__.ActiveUIDocument.Document)\
# #         .OfClass(DB.Wall)\
# #         .WhereElementIsNotElementType()\
# #         .ToElements()


# # print('\n## list of DB.Walls:')
# # for wall in cl:
# #     print(f'{wall} id:{wall.Id.IntegerValue}')


# print('\n## Output from csv')
# import csv
# csvfile = csv.reader(open("C:\\TEMP\\revit\\csv.csv", 'rb'), delimiter=';')

# for row in csvfile:
#     print(row)

# import json
# jsonfile = json.load(open("C:\\TEMP\\bsdd\\db.json"))

# print(jsonfile)



