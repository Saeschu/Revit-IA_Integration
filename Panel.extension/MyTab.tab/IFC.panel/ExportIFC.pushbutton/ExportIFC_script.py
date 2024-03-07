#! python3

### SATART of CODE ImportIDS ###
print('\n### SATART of CODE ImportIDS ###')
##############################################################################

# Import necesseray libraris
import ifcopenshell
import ifctester
from ifctester import ids, reporter
import os
import json
import csv
import System
import clr

from Autodesk.Revit.DB import *

# Application Members
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application

##############################################################################
class GetIDSFile:
    def __init__(self):
        self.directory = 'C:\\temp\\revit'
        self.names =  ['']
        self.files = {} 

        for filename in os.listdir(self.directory):
            if os.path.isfile(os.path.join(self.directory, filename)):
                if str(filename).endswith('.xml'):
                    self.names.append(str(filename.split('.')[0]).encode('utf-8'))
                    self.files[filename.split('.')[0]] = str(os.path.join(self.directory, filename)).encode('utf-8)')


                    
class MyIfcExport:
    def __init__(self, FilePath, IDSName):
        self.IDSName = str(IDSName).encode('utf-8')
        self.FilePath = str(FilePath).encode('utf-8')
        self.IFCName = str(f'IfcExport_{IDSName}').encode('utf-8')
        self.IfcFile = str(f'{self.FilePath}\\{self.IFCName}.ifc').encode('utf-8')
        self.ExportUserDefinedPsetsFile = str(f'C:\\ProgramData\\Autodesk\\ApplicationPlugins\\IFC 2021.bundle\\Contents\\2021\\IDSPropertySetDefined_{self.IDSName}.txt').encode('utf-8')
        


    def IfcExport(self):
        print('Informationsanforderung : ' + str(self.ExportUserDefinedPsetsFile))
        
        MyIfcExportOption = IFCExportOptions()
        MyIfcExportOption.SpaceBoundaryLevel = 0
        MyIfcExportOption.FileVersion = IFCVersion.IFC4DTV
        MyIfcExportOption.ExportBaseQuantities = False

        MyIfcExportOption.AddOption("StoreIFCGUID", "True")
        MyIfcExportOption.AddOption("UseFamilyAndTypeNameForReference", "False")
        # # MyIfcExportOption.AddOption("AssignAddressToBuilding", "True")
        MyIfcExportOption.AddOption("ExportInternalRevitPropertySets", "False")
        MyIfcExportOption.AddOption("ExportIFCCommonPropertySets", "False")
        MyIfcExportOption.AddOption("ExportUserDefinedPsets", "True")
        MyIfcExportOption.AddOption("ExportUserDefinedPsetsFileName", self.ExportUserDefinedPsetsFile )
        MyIfcExportOption.AddOption("VisibleElementsOfCurrentView", "True")
        MyIfcExportOption.AddOption("ExportRoomsInView", "True")
        MyIfcExportOption.AddOption("Use2DRoomBoundaryForVolume", "True")


        status = doc.Export(self.FilePath, self.IFCName, MyIfcExportOption)
        return status

##############################################################################
#__Main__
print("Informationsanforderung auswaehlen um dazupassenden IFC Export auszuloesen")

for item in GetIDSFile().names:
    print(item)

# IDSName = str(input('Eingabe IDS Name: '))
IDSName = 'IDS'
print(IDSName)

# TargetFolder = str(input ('Eingabe Speicherpfad für IfcDatei: '))
TargetFolder = "C:\\Users\\Sascha Hostettler\\Downloads"
print(TargetFolder)

MyExport = MyIfcExport(TargetFolder, IDSName)
IDSFiles = GetIDSFile().files
IfcFile = str(str(f'{TargetFolder}\\\\IfcExport_{IDSName}.ifc').encode('utf-8'))
print(IfcFile)


if TargetFolder and IDSName:
    # Start Transaction:
    t = Transaction(doc, "Add Parameters from IDS to Wall-elements")
    t.Start()

    print("export :" + str(MyExport.IfcExport()))

    t.Commit()


MyIfc = ifcopenshell.open(IfcFile)
MyIDS = ifctester.open(IDSFiles[IDSName])

# validate IFC model against IDS requirements:
MyIDS.validate(MyIfc)

# show results:
reporter.Console(MyIDS).report()
# ENDE of CODE ###
print('\n### ENDE of CODE ###')
