#! python3
from pyrevit import EXEC_PARAMS, DB
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
import System
from System import Enum

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application

elementId = uidoc.Selection.GetElementIds()[0].Value

element = doc.GetElement(ElementId(elementId))
# ElementTypeId = element.GetTypeId()
# elementType = doc.GetElement(ElementTypeId)
# cat = element.Category.Name


RevitParamter = element.LookupParameter('FM waveware Spital.Flaechenkategorie_SIA416')
print(RevitParamter)
t = Transaction(doc, "Ergaenze Classification Parameter")
t.Start()
RevitParamter.Set('Test123')

t.Commit()