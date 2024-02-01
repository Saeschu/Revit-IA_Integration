#imoprt pyrevit libraries
from pyrevit import revit, DB
from pyrevit import forms,script, EXEC_PARAMS
from pyrevit.forms import WPFWindow
from Autodesk.Revit.DB import Transaction

import System
from System import Enum
#imoprt python libraries



#functions

#Variabels
target_params = ["CoreIdentifier", "Impedence"]
target_bipgs = ["PG_IDENTITY_DATA", "INVALID"]

#Dummy data
instances = [True, False]
formulae = ["\"TEST1\"", "\"TEST2\""]



# Get shared parameters
app = __revit__.Application

defs  = []
I_bipgs = []

# Get all definitions and names
spFile   = app.OpenSharedParameterFile()
spGroups = spFile.Groups

sp_defs, sp_names = [],[]

for g in spGroups:
	for d in g.Definitions:
		sp_defs.append(d)
		sp_names.append(d.Name)
		
#get target definitions
defs = []
for t in target_params:
	if t in sp_names:
		ind = sp_names.index(t)
		defs.append(sp_defs[ind])

#Catch if we missed a definitions
if len(defs) != len(target_params):
	forms.alert("Some definitons not found, refer to report.", title="Script canceled")
		# Show what was missing...
	print("NOT FOUND IN SHARED PARAMETERS FILE:")
	print("---")
	for t in target_params:
		if t not in sp_names:
			print(t)
	script.exit()
	
# Get all bipgs for checking
bipgs = [a for a in System.Enum.GetValues(DB.BuiltInParameterGroup)]
bipg_names = [str(a) for a in bipgs]

for t in target_bipgs:
	if t in bipg_names:
		ind = bipg_names.index(t)
		I_bipgs.append(bipgs[ind])
		
# Catch if we don't have all BIPG's
if len(I_bipgs) != len(target_bipgs):
	forms.alert("Some groups not found, refer to report for details.", title="Script cancelled")
	# Show what was missing...
	print("NOT A VALID PARAMETER GROUP NAME:")
	print("---")
	for t in target_bipgs:
		if t not in bipg_names:
			print(t)
	script.exit()
	

	
#Add to current document
doc = revit.doc

# Define the parameter name and type
param_name = "MyWallParameter"

# Use the ParameterType from Autodesk.Revit.DB namespace
# param_type = DB.ParameterType.Text


# Check if the parameter already exists
existing_param = doc.ParameterBindings.get_Item(DB.BuiltInCategory.OST_Walls).get_Item(param_name)
print(existing_param)