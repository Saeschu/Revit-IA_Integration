### SATART of CODE ImportIDS ###
print('\n### SATART of CODE ImportIDS ###')
##############################################################################

# Import necessary Revit API classes
from pyrevit import revit, DB, forms,script, EXEC_PARAMS
from pyrevit.forms import WPFWindow
from Autodesk.Revit.DB import *
import System
# from System import *

import clr
import json
import csv


# Application Members
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application


##############################################################################

def set_new_parameter_to_Category(app, doc, spFile, RevitCatecory, paramterGroupName, parameter_name, paramter_DataType, tooltip, my_categories):
    
    for builtinCategory in System.Enum.GetValues(DB.BuiltInCategory):
        
        try: 
            
            if str(DB.LabelUtils.GetLabelFor(builtinCategory)).upper().encode('utf-8') == str(RevitCatecory).upper().encode('utf-8'):

                print( str('\nAnlegen von : : ') + str(DB.LabelUtils.GetLabelFor(builtinCategory)) + str (builtinCategory) + ' \t ' +  str(RevitCatecory) + '\t ' + str(parameter_name) )
                
                # Use BuiltInCategory to get the category 
                my_category = Category.GetCategory(doc, builtinCategory) 
                my_categories.Insert(my_category)
                
                break
        except:
            instance_bind_ok = False
            builtinCategory = None
            
            pass
        

    if builtinCategory != None:

        # Get the BindingMap of the current document
        binding_map = doc.ParameterBindings
        print('bindung_map : ', binding_map)
        # # Create a category set and insert the category into it
        # my_categories = app.Create.NewCategorySet()

        

        #Check if a ParameterBindung of paramter_name already Exist
        iterator = binding_map.ForwardIterator()
        ExistParamterBindung = False
        while (iterator.MoveNext()):

            if iterator.Key.Name == parameter_name:

                CategorySet = iterator.Current.Categories
                ExistParamterBindung = CategorySet.Contains(my_category)

        print('ExistParamterBindung ', parameter_name, ExistParamterBindung)
        
        if ExistParamterBindung == False:
            print(" Paramter will be added to Category ", my_category.Name, my_category)

        
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

            for binding in instance_binding.Categories:
                print(str('\t') + str(binding.Name))
        
            # Bind the definitions to the document
            instance_bind_ok = binding_map.Insert(my_definition_product_date,
                                                instance_binding, BuiltInParameterGroup.PG_IFC)
            
        
            print("     instance_bind_ok binded to the document:   ", instance_bind_ok)
        

    return instance_bind_ok

##############################################################################
##############################################################################
#handeling db
IDSName = 'IDS'
ProjectFilePath = 'C:\\temp\\revit'

dbJsonFile = str(ProjectFilePath) + str('\\db.json')
IdsXmlFile = str(ProjectFilePath) + str('\\') + str(IDSName) + str('.xml')


IDSPropertySetDefinedFolderPath = "C:\\ProgramData\\Autodesk\\ApplicationPlugins\\IFC 2021.bundle\\Contents\\2021"
IDSPropertySetDefinedFileName = str('IDSPropertySetDefined_') + str(IDSName)


#Creat dbDataFrame
dbJsonObject = open(dbJsonFile, "r")
dbDataFrame = json.load(dbJsonObject)


# Creat dataframe for IDSPropertySetDefined in Revit
# try:
RevitParameterMappingDataFrame = list( csv.reader(open(str(IDSPropertySetDefinedFolderPath) + str('\\') + str(IDSPropertySetDefinedFileName) + str('.txt'), 'r'), delimiter='\t')  )
# except:
#     print('ERROR: Es ist kein IDSPropertySetDefinedFileName vorhanden')


##############################################################################
####
##Spezifikationen zum Anlegen der Revit Parameter
spFile   = app.OpenSharedParameterFile()
paramterGroupName = "IR-FM_fromIDS"
paramter_DataType = SpecTypeId.String.Text
tooltip ="Tag: IDS, Description: Parameter Creadet from IDS Requirement"
####


##############################################################################

##__MAIN__##

# Start Transaction:
t = Transaction(doc, "Add Parameters from IDS to Wall-elements")
t.Start()

print('## IDSArg Keys')
print(dbDataFrame['IDSArg'].keys())
print('##')

print('\n## Verarbeite Attribute')
for entity in dbDataFrame['IDSArg'].keys():

    if entity.upper().encode('utf-8') in dbDataFrame['IfcMapping']:
        IfcEentity = entity.upper().encode('utf-8')
        RevitCatecories = dbDataFrame['IfcMapping'][entity.upper().encode('utf-8')]

        # print(str('\n') + str(IfcEentity) + ' : ' + str(RevitCatecories))

        for attribut in dbDataFrame['IDSArg'][entity]:
            RevitParamter = attribut
            
            # Create a category set and insert the category into it
            my_categories = app.Create.NewCategorySet()
            # print(str('\t') + str(attribut) + ' : ' + str(RevitParamter) )

            for RevitCatecory in RevitCatecories:
                if str(RevitCatecory).upper() != 'KEIN PASSENDE REVIT CATEGORY GEFUNDEN':
                    # print(str('\n') + str(RevitCatecory))
                    set_new_parameter_to_Category(app, doc, spFile, RevitCatecory, paramterGroupName, RevitParamter, paramter_DataType, tooltip, my_categories)
                


print('\n## Verarbeite Properties')
pos = 0
for line in RevitParameterMappingDataFrame:

    if line[0] == 'PropertySet:':

        for entity in line[3].split(','):
            if entity.upper().encode('utf-8') in dbDataFrame['IfcMapping']:
                IfcEentity = entity.upper().encode('utf-8')
                RevitCatecories = dbDataFrame['IfcMapping'][entity.upper().encode('utf-8')]
                IfcPropertySet = line[1]

                # Create a category set and insert the category into it
                my_categories = app.Create.NewCategorySet()

                # print(str('\n') + str(IfcEentity) + ' : ' + str(RevitCatecories))
                # print(str('\n') + str(IfcPropertySet) )

                for subline in RevitParameterMappingDataFrame[pos + 1:]:

                    if subline[0] =='':
                        IfcProperty = subline[1]
                        RevitParamter = subline[3]
                        # print(str('\t') + str(IfcProperty) + ' : ' + str(RevitParamter) )

                        for RevitCatecory in RevitCatecories:
                            if str(RevitCatecory).upper()  != 'KEIN PASSENDE REVIT CATEGORY GEFUNDEN':
                                # print(str('\n') + str(RevitCatecory))
                                set_new_parameter_to_Category(app, doc, spFile, RevitCatecory, paramterGroupName, RevitParamter, paramter_DataType, tooltip, my_categories)



                    else:
                        break


    pos = pos + 1
                   

# End Transaction:
t.Commit()

##############################################################################

# jsonString = json.dumps(dbDataFrame)
# dbJsonObject.write(jsonString)
dbJsonObject.close()

##############################################################################

### ENDE of CODE ###
print('\n### ENDE of CODE ###')

