import clr
clr.AddReference('System.Windows.Forms')
clr.AddReference('IronPython.Wpf')

import wpf

from pyrevit import EXEC_PARAMS, DB, UI, Forms, script
import System
from System import Enum
from System import Windows

import csv
##############################################################################

# Application Members
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application
output = script.get_output()
##############################################################################

### Variables
IDSName = "IDS"

xml_filename = script.get_bundle_file('ui.xaml')

IsIDScheckingPath = "C:\\temp\\revit\\IsIDSChecking.json"
idsxml = "C:\\temp\\revit\\ids.xml"
dbPath = "C:\\temp\\revit\\db.json"

IDSPropertySetDefinedFolderPath = "C:\\ProgramData\\Autodesk\\ApplicationPlugins\\IFC 2021.bundle\\Contents\\2021"
IDSPropertySetDefinedFileName = str('IDSPropertySetDefined_') + str(IDSName)

RevitParameterMappingDataFrame = list( csv.reader(open(str(IDSPropertySetDefinedFolderPath) + str('\\') + str(IDSPropertySetDefinedFileName) + str('.txt'), 'r'), delimiter='\t')  )

##############################################################################

#Template
# class MyWindow(Windows.Window):
#     def __init__(self):
#         wpf.LoadComponent(self, xml_filename )

#     def say_hello(self, sender, args):
#         InputText = self.texbox.Text
#         UI.TaskDialog.Show("Hello World", "Hello {}".format(InputText))

# MyWindow().ShowDialog()

class MyWindow(Windows.Window):
    def __init__(self):
        wpf.LoadComponent(self, xml_filename )

    def say_hello(self, sender, args):
        InputText = self.texbox.Text
        UI.TaskDialog.Show("Hello World", "Hello {}".format(InputText))

MyWindow().ShowDialog()


# class PropertySetDefinition():
#     def __init__(self, line, subline):
#         self.PropertySetName = line[1]
#         self.Typing = line[2]
#         self.Entity = line[3]
#         self.PropertyName = subline[1]
#         self.PropertyDataType = subline[2]
#         self.RevitParameterName = subline[3]


# for line in RevitParameterMappingDataFrame:
#     if line[0] == 'PropertySet:':

#         for subline in RevitParameterMappingDataFrame:
#             definition = PropertySetDefinition(line, subline)

# output.print_table(table_data=RevitParameterMappingDataFrame,
#                    title="Example Table",
#                    columns=["Row Name", "Column 1", "Column 2", "Percentage"],
#                    formats=['', '', '', '{}%'],
#                    )

