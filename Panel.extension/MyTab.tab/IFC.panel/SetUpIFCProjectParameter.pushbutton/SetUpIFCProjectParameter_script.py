
##############################################################################
# Import necessary Revit API classes
from pyrevit import revit, DB
from pyrevit import forms,script, EXEC_PARAMS
from pyrevit.forms import WPFWindow
from Autodesk.Revit.DB import *
import System
from System import Enum
import clr
##############################################################################

##############################################################################
def set_new_parameter_to_instance_wall(app, spFile, paramterGroupName, parameter_name, paramter_DataType, tooltip):
  
    # Create a new group in the shared parameters file

    my_groups = spFile.Groups
   
    all_groups = {}
    for group in my_groups:
        all_groups = {group.Name : group}


    if paramterGroupName not in all_groups:
        my_group = my_groups.Create(paramterGroupName)
        print("Group created")

    else:
        my_group = all_groups[paramterGroupName]
        print("Group alread existed")      

    # Create an instance definition in definition group MyParameters

    all_paramters ={}
    for parameter in my_group.Definitions:
        all_paramters = {parameter.Name : parameter}


    if parameter_name  not in all_paramters:

        option = ExternalDefinitionCreationOptions(parameter_name, paramter_DataType)
        
        # Set tooltip
        option.Description = tooltip
    
        try:
            my_definition_product_date = my_group.Definitions.Create(option)
            print("Parameter created")
        except:
            print("Binding already exist")


    else:
        my_definition_product_date = all_paramters[parameter_name]
        print("Parameter allready existed")


    # Create a category set and insert the category of wall into it
    my_categories = app.Create.NewCategorySet()

    # Use BuiltInCategory to get the category of wall
    my_category = Category.GetCategory(doc, BuiltInCategory.OST_ProjectInformation)


    my_categories.Insert(my_category)

    # Create an instance of InstanceBinding
    instance_binding = app.Create.NewInstanceBinding(my_categories)
    print("instance_binding", instance_binding)

    # Get the BindingMap of the current document
    binding_map = doc.ParameterBindings
    # Bind the definitions to the document
    instance_bind_ok = binding_map.Insert(my_definition_product_date,
                                        instance_binding, BuiltInParameterGroup.PG_IFC)
    
    print("instance_bind_ok", instance_bind_ok)
    
    return instance_bind_ok


##############################################################################

##############################################################################
# Application Members
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application
##############################################################################
#Imput Data
# parameterlistFromIDS = ['IfcGUID', 'IfcName', 'IfcDescription','IFC Predefined Typ', 'IfcObjectType']
parameterlistFromIDS = ["IfcDescription", "IfcObjectType", "SiteName", "SiteDescription", "SiteLandTitleNumber", "SiteLongName", "SiteObjectType", "BuildingDescription", "BuildingLongName", "BuildingObjectType" ]
####
spFile   = app.OpenSharedParameterFile()
paramterGroupName = "IR-FM_fromIDS"
paramter_DataType = SpecTypeId.String.Text
tooltip ="tooltiop, new Paramter for a Projectinformatin"
####


# print(IFCExportOptions.FamilyMappingFile())


#Main
##############################################################################

# spFile = app.SharedParameterElement.Creat(doc, )

# open current SharedParamterfile


# Start Transaction:
t = Transaction(doc, "Set up IFC STandard PArameter for IFCProject, IFCSite, IFCBuilding")
t.Start()

# Changes
for parameter_name in parameterlistFromIDS  :
    set_new_parameter_to_instance_wall(app, spFile, paramterGroupName, parameter_name, paramter_DataType, tooltip)
    print(parameter_name,  ' : ist sucsessfuly added to the Catecory Wall')

# End Transaction:
t.Commit()

##############################################################################

