
# ##############################################################################
# # Import necessary Revit API classes
from Autodesk.Revit.DB import *
from System import Guid

# ##############################################################################



# #Main
# ##############################################################################
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
app = __revit__.Application
spFile   = app.OpenSharedParameterFile()
# IDSName = input('eingabe IDS name der zu loeschenden Parameter : ')
IDSName = 'IDS'
paramterGroupName = str("IR-FM_fromIDS_") + str(IDSName)

# Retrieve all parameters in the document
params = FilteredElementCollector(doc).OfClass(ParameterElement)
filteredparams = []
paramterlist = []

my_groups = spFile.Groups
for my_group in my_groups:
    if my_group.Name == paramterGroupName:
        for parameter in my_group.Definitions:
            paramterlist.append(parameter.Name)

print(paramterlist)
# Store parameters which have a name starting with "magi" or "MC"
for param in params:

    # print(param.Name)
    # if param.Name.startswith("Ifc"):  # startswith method accepts tuple
    if param.Name in paramterlist:
        filteredparams.append(param)

# Start Transaction:
t = Transaction(doc, "Clear bindung_map")
t.Start()

for param in filteredparams:
    name = param.Name
    doc.Delete(param.Id)
    print(name, " is deleted")

# End Transaction:
t.Commit()
# ##############################################################################
print("Endo of Code")



