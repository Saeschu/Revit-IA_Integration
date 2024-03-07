### SATART of CODE ImportIDS ###
print('\n### SATART of CODE ImportIDS ###')
##############################################################################

# Import necessary Revit API classes
from pyrevit import revit, DB, forms, script, EXEC_PARAMS
# from pyrevit.forms import WPFWindow
from Autodesk.Revit.DB import *
import System
# from System import *

import clr
import json
import csv
import os


# Application Members
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application

output = script.get_output()
##############################################################################

def getImportedIDS():
    directory = 'C:\\temp\\revit'
    ImportedIDS = ['Exit']
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            if str(filename).endswith('.xml'):
                ImportedIDS.append(filename.split('.')[0])

    return ImportedIDS 

def CreatViewforIR(IDSName):
    #ALL VIEW TYPES
    view_types = FilteredElementCollector(doc).OfClass(ViewFamilyType).ToElements()

    #FILTER VIEW TYPES
    for view in view_types:
        if view.ViewFamily == ViewFamily.ThreeDimensional:
            view_type_3D = view

    View3DCollector = []
    for view in FilteredElementCollector(doc).OfClass(View3D):
        View3DCollector.append({view.Name : view})

    # Create 3D - Isometricview
    if IDSName not in View3DCollector:
        t = Transaction(doc,'Create 3D Isometric')
        t.Start() 
        view3D = View3D.CreateIsometric(doc, view_type_3D.Id) 
        view3D.Name = IDSName
        t.Commit()
        return True
    
    else:
        return False
        

    
    
def CreatMapping(RevitParameterMappingDataFrame):
    def showMapping(RevitParameterMappingDataFrame):
        DataSet = []

        for line in RevitParameterMappingDataFrame:
            if len(line) > 1 and line[0] == 'PropertySet:':
                print(line[1])
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


def ParamterBindungToBuiltInCategory(app, doc, spFile, builtinCategory, paramterGroupName, ParameterName, ParamterDataType, tooltip):
    
    # Get the BindingMap of the current document
    BindingMap = doc.ParameterBindings
    print(str("bindung_map : ") +  str(BindingMap))

    #### Temp, danach loeschen
    # Create a category set and insert the category into it
    MyCategories = app.Create.NewCategorySet()

    # Use BuiltInCategory to get the category 
    MyCategory = Category.GetCategory(doc, builtinCategory) 
    MyCategories.Insert(MyCategory)
    ####


    #Check if a ParameterBindung of paramter_name already Exist
    iterator = BindingMap.ForwardIterator()
    ExistParamterBindung = False

    while (iterator.MoveNext()):
        for category in MyCategories:
            if iterator.Key.Name == ParameterName:

                CategorySet = iterator.Current.Categories
                ExistParamterBindung = CategorySet.Contains(category)

                print(str("ExistParamterBindung ") +  str(ParameterName) + ' ' + str(ExistParamterBindung))
                instance_bind_ok = 'bereits vorhanden'
                    

    if ExistParamterBindung == False:
        print(str(" Paramter will be added to Category ") +  str(MyCategories))
  
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

        AllParamters = {}
        for parameter in my_group.Definitions:
            AllParamters[parameter.Name] = parameter

        if ParameterName  not in AllParamters:

            option = ExternalDefinitionCreationOptions(ParameterName, ParamterDataType)
            
            # Set tooltip
            option.Description = tooltip
            MyDefinitionProductDate = my_group.Definitions.Create(option)
            
            print(str("     Parameter created:  ") +  str(ParameterName))


        else:

            MyDefinitionProductDate = AllParamters[ParameterName]
            
            print(str("\tParameter allready exist:  ") + str(MyDefinitionProductDate) + ' ' + str(AllParamters[ParameterName]))

            print(str("\tExist Parameter bindung : ") +  str(BindingMap.Contains(MyDefinitionProductDate) ))

        # Create an instance of InstanceBinding for the Parameter
        InstanceBinding = app.Create.NewInstanceBinding(MyCategories)
        print(str("\tinstance_binding Created: ")  + str(InstanceBinding))

        # Bind the definitions to the document
        instance_bind_ok = BindingMap.Insert(MyDefinitionProductDate,
                                            InstanceBinding, BuiltInParameterGroup.PG_IFC)
        
    
        print(str("\tinstance_bind_ok binded to the document: ") + ' ' + str( instance_bind_ok) +  '( ' + str( MyCategory.Name ) + ' : ' + str(MyDefinitionProductDate.Name) +  ' )' )
    

    return instance_bind_ok

##############################################################################
##############################################################################

IDSName = forms.CommandSwitchWindow.show(getImportedIDS(),  message='IDS Auswählen um dessen Parameter anzulegen')
# IDSName = 'IDS'
#handeling db
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
CreatViewforIR(IDSName)

##__MAIN__##
print()
# Start Transaction:
t = Transaction(doc, "Add Parameters from IDS to Categories")
t.Start()

print('## IDSArg Keys')
print(dbDataFrame[IDSName]['IDSArg'].keys())
print('##')

print('\n## Verarbeite Attribute')
for entity in dbDataFrame[IDSName]['IDSArg'].keys():

    if entity.upper().encode('utf-8') in dbDataFrame[IDSName]['IfcMapping']:
        IfcEentity = entity.upper().encode('utf-8')
        RevitCatecories = dbDataFrame[IDSName]['IfcMapping'][entity.upper().encode('utf-8')]

        for attribut in dbDataFrame[IDSName]['IDSArg'][entity]:
            RevitParamter = attribut

            for RevitCatecoryName in RevitCatecories:
                if len(RevitCatecoryName.split('\t')) == 1:
                    print(str('\n') + str(RevitCatecoryName))
                    builtInCategory = GetBuiltInCatecory(RevitCatecoryName)
                    ParamterBindungToBuiltInCategory(app, doc, spFile, builtInCategory, paramterGroupName, RevitParamter, paramter_DataType, tooltip)
                


print('\n## Verarbeite Properties')
pos = 0
for line in RevitParameterMappingDataFrame:

    if line[0] == 'PropertySet:':

        for entity in line[3].split(','):
            print(entity)
            if entity.upper().encode('utf-8') in dbDataFrame[IDSName]['IfcMapping']:
                IfcEentity = entity.upper().encode('utf-8')
                RevitCatecories = dbDataFrame[IDSName]['IfcMapping'][IfcEentity] #['Rooms', 'Spaces'] #
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

