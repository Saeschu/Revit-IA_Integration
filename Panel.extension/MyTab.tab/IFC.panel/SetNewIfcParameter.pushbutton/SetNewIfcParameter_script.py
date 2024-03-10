### SATART of CODE ImportIDS ###
#Autor: Sascha Hostettler
#Datum: 20.05.2024
#Version: ?
#Beschrieb: 
#
#
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
class FamilyOption(IFamilyLoadOptions):
    def OnFamilyFound(self, familyInUse, overwriteParameterValues):
        overwriteParameterValues = True
        return True

    def OnSharedFamilyFound(self, sharedFamily, familyInUse, source, overwriteParameterValues):
        return True
    

class GetFamily():
    def __init__(self, doc, IRTypeName):
        self.IRTypeName = IRTypeName
        self.familyDoc = None
        self.famMan = None
               
        # Erstellen eines collectors alle Familien
        collector = FilteredElementCollector(doc)
        collector.OfClass(Family)
        
        #Alle Elemente der Familien
        families = collector.ToElements()
        for family in families:
            # print(family.Name)
            # if family.Name == "Pumpe allgemein - Gewinde":
            #     print(family)
            #     print(family.GetFamilySymbolIds())
            for id in family.GetFamilySymbolIds():
                ElementId = doc.GetElement(id)
                try:
                    IfcTypeName = ElementId.LookupParameter('Export Type to IFC As').AsString()
                except:
                    pass
      
                #Pruefen ob der Export Typ to IFC der IFcEntitaet welche in der IR gefordert wird entspricht
                #ToDo: Spaeter zu einer Liste umbauen, um alle Familien zu finden nicht nur die erste
                if IfcTypeName != None and IfcTypeName.upper().encode('utf-8') == self.IRTypeName:
                    self.familyDoc = doc.EditFamily(family)
                    if self.familyDoc.IsFamilyDocument:
                        self.famMan = self.familyDoc.FamilyManager
                        print('Is FamilyDoc', self.famMan)

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
    t = Transaction(doc, str("Add Parameters from IDS to Categories : {}").format(ParameterName ))
    t.Start()
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
        myGroups = spFile.Groups
    
        allGroups = {}
        for group in myGroups:
            allGroups[group.Name] = group

        if paramterGroupName not in allGroups:
            myGroup = myGroups.Create(paramterGroupName)
            print(str("     Group created:  ") + str(myGroup.Name))

        else:
            myGroup = allGroups[paramterGroupName]
            print(str("     Group alread exist: ") +  str(myGroup.Name))      


        # Create an instance definition of the Parameter in definition group MyParameters

        AllParamters = {}
        for parameter in myGroup.Definitions:
            AllParamters[parameter.Name] = parameter

        if ParameterName  not in AllParamters:

            option = ExternalDefinitionCreationOptions(ParameterName, ParamterDataType)
            
            # Set tooltip
            option.Description = tooltip
            MyDefinitionProductDate = myGroup.Definitions.Create(option)
            
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
        #End Transaction:               
        t.Commit()
        
    
        print(str("\tinstance_bind_ok binded to the document: ") + ' ' + str( instance_bind_ok) +  '( ' + str( MyCategory.Name ) + ' : ' + str(MyDefinitionProductDate.Name) +  ' )' )
    

    return instance_bind_ok


def CreatFamilyParameter(familyDoc, famMan, myFamParameter, paramterGroupName, paramterDataType):
    t = Transaction(familyDoc, "CreatFamilyParameter")
    t.Start()


    #Oeffnen des ScheredParamter Files
    spFile = app.OpenSharedParameterFile()
    myGroups = spFile.Groups

    
    #Pruefen ob die Gruppe beretis vorhanden ist oder nicht, anosten neu anlegen
    allGroups = {}
    for group in myGroups:
        allGroups[group.Name] = group

    if paramterGroupName not in allGroups:
        myGroup = myGroups.Create(paramterGroupName)
        print(str("     Group created:  ") + str(myGroup.Name))

    else:
        myGroup = allGroups[paramterGroupName]
        print(str("     Group alread exist: ") +  str(myGroup.Name))


    #Pruefen ob der Parameter beretis vorhanden ist oder nicht, anosten neu anlegen
    AllFamParamters = {}
    for parameter in myGroup.Definitions:
        AllFamParamters[parameter.Name] = parameter

    if myFamParameter  not in AllFamParamters:
        option = ExternalDefinitionCreationOptions(myFamParameter, paramterDataType)
        MyDefinitionProductDate = myGroup.Definitions.Create(option)

        MyExternalDefintion = myGroup.Definitions.get_Item(myFamParameter) 
        print(str("Family Parmeter neu in SharedParamterfile angelegt: ") +  str(myFamParameter))
    
        #Pruefen ob eine externe Definition erstellt werden konnte
        if MyExternalDefintion != None:
            famMan.AddParameter(MyExternalDefintion, BuiltInParameterGroup.PG_IFC, False)

            #End Transaction:               
            t.Commit()
            print(str("Family Parmeter neu erstellt: ") +  str(myFamParameter))
            # Laden der geaenderten Familie in das Projektdokument
            familyDoc.LoadFamily(doc, FamilyOption())
            familyDoc.Close(True)  
            print(str("FamilyDoc ist gespeichert und neu geladen: ") +  str(familyDoc))
            return True
        
        else:
            print('MyExternalDefintion kann nicht Null sein')
            t.RollBack()
            return False
        
    else:
        MyExternalDefintion = AllFamParamters[myFamParameter]
        famMan.AddParameter(MyExternalDefintion, BuiltInParameterGroup.PG_IFC, False)
        t.Commit()
        familyDoc.LoadFamily(doc, FamilyOption())
        familyDoc.Close(True)  
        print(str("Family Parmeter ist in SharedPArameterfile bestehend: ") +  str(myFamParameter))
        
        return True


##############################################################################
##############################################################################

IDSName = forms.CommandSwitchWindow.show(getImportedIDS(),  message='IDS Auswaehlen um dessen Parameter anzulegen')
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
paramterDataType = SpecTypeId.String.Text
tooltip ="Tag: IDS, Description: Parameter Creadet from IDS Requirement"
####


##############################################################################

CreatMapping(RevitParameterMappingDataFrame)
try:
    CreatViewforIR(IDSName)
    print(str('Ansicht {} neu erstellt').format(IDSName))
except:
    print('Ansicht existiert bereits')
##__MAIN__##
print()
# Start Transaction:
# t = Transaction(doc, "Add Parameters from IDS to Categories")
# t.Start()

print('## IDSArg Keys')
print(dbDataFrame[IDSName]['IDSArg'].keys())
print('##')

print('\n## Verarbeite Attribute')
for entity in dbDataFrame[IDSName]['IDSArg'].keys():

    if entity.upper().encode('utf-8') in dbDataFrame[IDSName]['IfcMapping']:
        if entity.upper().encode('utf-8').endswith('TYPE'):
            print('Creat new Family Parameter')
            MyFamily = GetFamily(doc, entity.upper().encode('utf-8'))
            print(MyFamily.familyDoc)

            for attribut in dbDataFrame[IDSName]['IDSArg'][entity]:
                myFamParameter = attribut
                CreatFamilyParameter(MyFamily.familyDoc, MyFamily.famMan, myFamParameter, paramterGroupName, paramterDataType)


        else:

            IfcEentity = entity.upper().encode('utf-8')
            RevitCatecories = dbDataFrame[IDSName]['IfcMapping'][entity.upper().encode('utf-8')]

            for attribut in dbDataFrame[IDSName]['IDSArg'][entity]:
                RevitParamter = attribut

                for RevitCatecoryName in RevitCatecories:
                    if len(RevitCatecoryName.split('\t')) == 1:
                        print(str('\n') + str(RevitCatecoryName))
                        builtInCategory = GetBuiltInCatecory(RevitCatecoryName)
                        ParamterBindungToBuiltInCategory(app, doc, spFile, builtInCategory, paramterGroupName, RevitParamter, paramterDataType, tooltip)
                


print('\n## Verarbeite Properties')
pos = 0
for line in RevitParameterMappingDataFrame:

    if line[0] == 'PropertySet:':
        if line[3].startswith('['):
            line3 = line[3][2:-2].split(',')

        else:
            line3 = line[3].split(',')

        for entity in line3:
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

                        if len(RevitCatecories) == 0:
                            if entity.upper().encode('utf-8').endswith('TYPE'):
                                print('Creat new Family Parameter')
                                myFamParameter = RevitParamter
                                MyFamily = GetFamily(doc, entity.upper().encode('utf-8'))
                                print(MyFamily.familyDoc, MyFamily.famMan, myFamParameter)
                                CreatFamilyParameter(MyFamily.familyDoc, MyFamily.famMan, myFamParameter, paramterGroupName, paramterDataType)
              

                            else:
                                print('kein Mapping vorhandne, pruefen Sie das IDS und die Revit Mappingkonfiguration')
                        
                        else:
                            for RevitCatecoryName in RevitCatecories:
                                                    
                                if len(RevitCatecoryName.split('\t')) == 1:
                                    print(str('\n') + str(RevitCatecoryName) + ' :  ' + str(RevitParamter))

                                    builtInCategory = GetBuiltInCatecory(RevitCatecoryName)
                                    ParamterBindungToBuiltInCategory(app, doc, spFile, builtInCategory, paramterGroupName, RevitParamter, paramterDataType, tooltip)

                    else:
                        break


    pos = pos + 1
              
# End Transaction:
# t.Commit()

##############################################################################

# jsonString = json.dumps(dbDataFrame)
# dbJsonObject.write(jsonString)
dbJsonObject.close()


csv_writer = csv.writer(open(str(IDSPropertySetDefinedFolderPath) + str('\\') + str(IDSPropertySetDefinedFileName) + '.txt', 'w'), delimiter='\t', quoting=csv.QUOTE_MINIMAL)
csv_writer.writerows(RevitParameterMappingDataFrame)
##############################################################################

### ENDE of CODE ###
print('\n### ENDE of CODE ###')

