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

output = script.get_output()
##############################################################################
class CreatRevitParameter:
    def __init__(self):
        self.Apfel = 'Apfel'

def CreatMapping(RevitParameterMappingDataFrame):
    def showMapping(RevitParameterMappingDataFrame):
        DataSet = []

        for line in RevitParameterMappingDataFrame:
            if line[0] == 'PropertySet:':

                for subline in RevitParameterMappingDataFrame:
                    DataSet.append([line[1], subline[1], subline[3]])

        output.print_table(table_data=DataSet,
                    title="Property Mapping Table",
                    columns=["IfcPropertySet", "IfcPropertyName", "RevitParamterName"],
                    formats=['', '', '{}'])

    showMapping(RevitParameterMappingDataFrame)
    InputMapping = 'None'
    while InputMapping.upper() != 'SAVE':
        for line in RevitParameterMappingDataFrame:
            if str(line[1]).upper() == InputMapping.split(' ')[0].upper():
                line[3] = InputMapping.split(' ')[1]
                showMapping(RevitParameterMappingDataFrame)
                break  

        InputMapping = raw_input('Mapping: <IfcProperty> <newRevitParameterName> (um zu Stoppen "SAVE" eingeben)')

    return RevitParameterMappingDataFrame


def GetBuiltInCatecory(RevitCatecoryName):
    # Create a category set and insert the category into it
    # my_categories = app.Create.NewCategorySet()

    for builtinCategory in System.Enum.GetValues(DB.BuiltInCategory):
        
        try: 
            
            if str(DB.LabelUtils.GetLabelFor(builtinCategory)).upper().encode('utf-8') == str(RevitCatecoryName).upper().encode('utf-8'):

                print( str('\nAnlegen von : ') + str(RevitCatecoryName) + '\t ' + str (builtinCategory))
                
                break
        except:          
            pass

    return builtinCategory


def ParamterBindungToBuiltInCategory(app, doc, spFile, builtinCategory, paramterGroupName, parameter_name, paramter_DataType, tooltip):
    
    # Get the BindingMap of the current document
    binding_map = doc.ParameterBindings
    print(str("bindung_map : ") +  str(binding_map))

    #### Temp, danach loeschen
    # Create a category set and insert the category into it
    my_categories = app.Create.NewCategorySet()

    # Use BuiltInCategory to get the category 
    my_category = Category.GetCategory(doc, builtinCategory) 
    my_categories.Insert(my_category)
    ####


    #Check if a ParameterBindung of paramter_name already Exist
    iterator = binding_map.ForwardIterator()
    ExistParamterBindung = False

    while (iterator.MoveNext()):
        for category in my_categories:
            if iterator.Key.Name == parameter_name:

                CategorySet = iterator.Current.Categories
                ExistParamterBindung = CategorySet.Contains(category)

                print(str("ExistParamterBindung ") +  str(parameter_name) + ' ' + str(ExistParamterBindung))
                instance_bind_ok = 'bereits vorhanden'
                    

    if ExistParamterBindung == False:
        print(str(" Paramter will be added to Category ") +  str(my_categories))
  
        # Create a new group in the shared parameters file if not allready exist
        my_groups = spFile.Groups
    
        all_groups = {}
        for group in my_groups:
            all_groups[group.Name] = group

        if paramterGroupName not in all_groups:
            my_group = my_groups.Create(paramterGroupName)
            print(str("     Group created:  ") + str(my_group.Name))

        else:
            my_group = all_groups[paramterGroupName]
            print(str("     Group alread exist: ") +  str(my_group.Name))      


        # Create an instance definition of the Parameter in definition group MyParameters

        all_paramters = {}
        for parameter in my_group.Definitions:
            all_paramters[parameter.Name] = parameter

        if parameter_name  not in all_paramters:

            option = ExternalDefinitionCreationOptions(parameter_name, paramter_DataType)
            
            # Set tooltip
            option.Description = tooltip
            my_definition_product_date = my_group.Definitions.Create(option)
            
            print(str("     Parameter created:  ") +  str(parameter_name))


        else:

            my_definition_product_date = all_paramters[parameter_name]
            
            print(str("\tParameter allready exist:  ") + str(my_definition_product_date) + ' ' + str(all_paramters[parameter_name]))

            print(str("\tExist Parameter bindung : ") +  str(binding_map.Contains(my_definition_product_date) ))

        # Create an instance of InstanceBinding for the Parameter
        instance_binding = app.Create.NewInstanceBinding(my_categories)
        print(str("\tinstance_binding Created: ")  + str(instance_binding))

        # Bind the definitions to the document
        instance_bind_ok = binding_map.Insert(my_definition_product_date,
                                            instance_binding, BuiltInParameterGroup.PG_IFC)
        
    
        print(str("\tinstance_bind_ok binded to the document: ") + ' ' + str( instance_bind_ok) +  '( ' + str( my_category.Name ) + ' : ' + str(my_definition_product_date.Name) +  ' )' )
    

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
paramterGroupName = str("IR-FM_fromIDS_") + str(IDSName)
paramter_DataType = SpecTypeId.String.Text
tooltip ="Tag: IDS, Description: Parameter Creadet from IDS Requirement"
####


##############################################################################

CreatMapping(RevitParameterMappingDataFrame)

##__MAIN__##
print()
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

        for attribut in dbDataFrame['IDSArg'][entity]:
            RevitParamter = attribut

            for RevitCatecoryName in RevitCatecories:
                if len(RevitCatecoryName.split('\t')) == 1:
                    print(str('\n') + str(RevitCatecoryName))
                    builtInCategory = GetBuiltInCatecory(RevitCatecoryName)
                    # ParamterBindungToBuiltInCategory(app, doc, spFile, builtInCategory, paramterGroupName, RevitParamter, paramter_DataType, tooltip)
                


print('\n## Verarbeite Properties')
pos = 0
for line in RevitParameterMappingDataFrame:

    if line[0] == 'PropertySet:':

        for entity in line[3].split(','):
            print(entity)
            if entity.upper().encode('utf-8') in dbDataFrame['IfcMapping']:
                IfcEentity = entity.upper().encode('utf-8')
                RevitCatecories = ['Rooms', 'Spaces'] #dbDataFrame['IfcMapping'][IfcEentity]
                print(RevitCatecories)
                IfcPropertySet = line[1]

                for subline in RevitParameterMappingDataFrame[pos + 1:]:

                    if subline[0] =='':
                        IfcProperty = str(subline[1]).encode('utf-8')

                        if subline[3] != '':
                            RevitParamter = str(subline[3]).encode('utf-8')
                        else:
                            RevitParamter = str(subline[1]).encode('utf-8')

 
                        for RevitCatecoryName in RevitCatecories:
                            if len(RevitCatecoryName.split('\t')) == 1:
                                print(str('\n') + str(RevitCatecoryName) + ' :  ' + str(RevitParamter))
                                builtInCategory = GetBuiltInCatecory(RevitCatecoryName)
                                ParamterBindungToBuiltInCategory(app, doc, spFile, builtInCategory, paramterGroupName, RevitParamter, paramter_DataType, tooltip)

                    else:
                        break


    pos = pos + 1
                   
# End Transaction:
t.Commit()

##############################################################################

# jsonString = json.dumps(dbDataFrame)
# dbJsonObject.write(jsonString)
dbJsonObject.close()


csv_writer = csv.writer(open(str(IDSPropertySetDefinedFolderPath) + str('\\') + str(IDSPropertySetDefinedFileName) + '.txt', 'w'), delimiter='\t', quoting=csv.QUOTE_MINIMAL)
csv_writer.writerows(RevitParameterMappingDataFrame)
##############################################################################

### ENDE of CODE ###
print('\n### ENDE of CODE ###')

