
# ##############################################################################
import os
import json

from Autodesk.Revit.DB import *
from pyrevit import forms
from System import Guid

class config():
    def __init__(self):
        ConfigPath = "C:\\Users\\Sascha Hostettler\\Documents\\GitHub\\pyRevit-IDS_bSDD\\Revit-IA_Integration\\Panel.extension\\lib\\config.json"
        with open(ConfigPath) as ConfigFile:
            Config = json.load(ConfigFile)

        self.TempPfad = Config['TempPfad']
        self.IsIDSChecking = Config['IsIDSChecking']


uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
app = __revit__.Application
spFile   = app.OpenSharedParameterFile()
# ##############################################################################

def getImportedIDS():
    directory = config().TempPfad
    ImportedIDS = ['Exit']
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            if str(filename).endswith('.xml'):
                ImportedIDS.append(filename.split('.')[0])

    return ImportedIDS 

###############################################################################
#__Main__
IDSName = forms.CommandSwitchWindow.show(getImportedIDS(),  message='zu Loeschendes IDS angeben')

if IDSName != 'Exit':

    paramterGroupName = str("IR-FM_fromIDS_") + str(IDSName)

    # Retrieve all parameters in the document
    params = FilteredElementCollector(doc).OfClass(ParameterElement)
    filteredparams = []
    paramterlist = []

    my_groups = spFile.Groups
    for my_group in my_groups:
        if my_group.Name == paramterGroupName:
            GroupToDelet = my_group
            for parameter in my_group.Definitions:
                paramterlist.append(parameter.Name)

    for param in params:
        if param.Name in paramterlist:
            filteredparams.append(param)

    # Start Transaction:
    t = Transaction(doc, "Clear bindung_map")
    t.Start()

    for param in filteredparams:
        name = param.Name
        doc.Delete(param.Id)
        print(str(name) +  " is deleted")


    # End Transaction:
    t.Commit()

    # ##############################################################################
    print("Endo of Code")

