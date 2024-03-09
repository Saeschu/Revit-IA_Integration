
from Autodesk.Revit.DB import *
from pyrevit import revit, DB, forms, script, EXEC_PARAMS  
import System
# from System import enum


IDSName = 'IDS'

#VARIABLES
doc          = __revit__.ActiveUIDocument.Document
active_view  = doc.ActiveView
active_level = doc.ActiveView.GenLevel

def CreatViewforIR(IDSName):
    #ALL VIEW TYPES
    view_types = FilteredElementCollector(doc).OfClass(ViewFamilyType).ToElements()

    for view in FilteredElementCollector(doc).OfClass(View3D):
        print(view.Name)


    #FILTER VIEW TYPES
    for view in view_types:
        if view.ViewFamily == ViewFamily.ThreeDimensional:
            view_type_3D = view

    View3DCollector = []
    for view in FilteredElementCollector(doc).OfClass(View3D):
        View3DCollector.append({view.Name : view})
    # Create 3D - Isometricview
    t = Transaction(doc,'Create 3D Isometric')
    t.Start()

    if IDSName not in View3DCollector:
        view3D = View3D.CreateIsometric(doc, view_type_3D.Id) 
        view3D.Name = IDSName
    else:
        pass
        

    t.Commit()
