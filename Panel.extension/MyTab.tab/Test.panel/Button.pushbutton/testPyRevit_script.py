

# from Autodesk.Revit.DB import *
from pyrevit import revit, DB, forms, script, EXEC_PARAMS  
import System
# from System import enum


import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')

from Autodesk.Revit.ApplicationServices import *
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
#  from Autodesk.Revit.DB import IFamilyLoadOptions, Family, FamilySource

# Application Members
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application


class FamilyOption(IFamilyLoadOptions):
    def OnFamilyFound(self, familyInUse, overwriteParameterValues):
        overwriteParameterValues = True
        return True

    def OnSharedFamilyFound(self, sharedFamily, familyInUse, source, overwriteParameterValues):
        return True
    
def get_all_families_in_project(doc):
    # Initialize a set to collect unique family names
    unique_families = set()

    # Retrieve all elements in the document
    collector = FilteredElementCollector(doc)

    # Filter elements by category (FamilyInstance)
    elements = collector.OfClass(FamilyInstance).ToElements()

    # Iterate through elements to extract family names
    for instance in elements:
        # Get the family symbol
        symbol = instance.Symbol

        # Get the family name
        family_name = symbol.Family.Name

        # Add the family name to the set
        unique_families.add(family_name)

    # Print or do something with the unique family names
    for family_name in unique_families:
        # TaskDialog.Show("Unique Family Name", family_name)
        print(("Unique Family Name", family_name))

# This method should be called from an external command or any other suitable context
def execute(command_data):
    doc = command_data.ActiveUIDocument.Document
    get_all_families_in_project(doc)

# Example of how to execute the code in pyRevit
# Replace with your appropriate context for executing the code
# execute(command_data)
execute(__revit__)

#############################################################################
print(30*'-')

import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')

from Autodesk.Revit.DB import FilteredElementCollector, Family
from pyrevit import revit, DB

def get_all_families(TypeName):
    # Get the active Revit document
    doc = revit.doc
    
    # Create a filtered element collector to collect all families

    collector = FilteredElementCollector(doc)
    collector.OfClass(Family)
    
    # Get the list of all families
    families = collector.ToElements()
    
    # Print out the names of all families
    for family in families:
        # print(family.Name)
        if family.Name == "Pumpe allgemein - Gewinde":
            print(family)
            print(family.GetFamilySymbolIds())
            for id in family.GetFamilySymbolIds():
                ElementId = doc.GetElement(id)

                IfcTypeName = ElementId.LookupParameter('Export Type to IFC As').AsString()

                if IfcTypeName == TypeName:
                    
                    familyDoc = doc.EditFamily(family)
                    print(familyDoc)
                    if familyDoc.IsFamilyDocument:
                        famMan = familyDoc.FamilyManager
                        print('Is FamilyDoc', famMan)

    return familyDoc

def CreatParamterInFamily(familyDoc, myFamParameter, paramterGroupName, paramter_DataType):
    t = Transaction(familyDoc, "my Transaction")
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
        option = ExternalDefinitionCreationOptions(myFamParameter, paramter_DataType)
        MyDefinitionProductDate = myGroup.Definitions.Create(option)

        MyExternalDefintion = myGroup.Definitions.get_Item(myFamParameter) 
        print(str("     Family Parmeter neu Erstellt: ") +  str(myFamParameter))
    
    else:
        MyExternalDefintion = AllFamParamters[myFamParameter]
        print(str("     Family Parmeter ist bestehend: ") +  str(myFamParameter))


    #Pruefen ob eine externe Definition erstellt werden konnte
    if MyExternalDefintion != None:
        famMan.AddParameter(MyExternalDefintion, BuiltInParameterGroup.PG_IFC, False)

    else:
        print('MyExternalDefintion kann icht Null sein')
        t.RollBack

    #End Transaction:               
    t.Commit()

    # Laden der geaenderten Familie in das Projektdokument
    familyDoc.LoadFamily(doc, FamilyOption())



                    



paramterGroupName = "FM_fromIDS_IDS"
myFamParameter = 'MyParameter_2'
paramter_DataType = SpecTypeId.String.Text
# Execute the function
get_all_families(myFamParameter)

