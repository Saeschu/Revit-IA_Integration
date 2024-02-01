# Import libraries
from pyrevit import DB, revit, script, forms

# Prompt user to specify file path
filterXcl = 'Excel workbooks|*.xlsx'
filterRfa = 'Family Files|*.rfa'

path_xcl = forms.pick_file(files_filter=filterXcl, title="Choose excel file")

if not path_xcl:
	script.exit()

# Prompt user to specify families
path_rfas = forms.pick_file(files_filter=filterRfa, multi_file=True, title="Choose families")

if not path_rfas:
	script.exit()

# Import Excel data
from guRoo_xclUtils import *

xcl = xclUtils([],path_xcl)
dat = xcl.xclUtils_import("Standard", 5, 0)

targets_params, target_bipgs, fam_inst, fam_formulae = [],[],[],[]

for row in dat[0][1:]:
	targets_params.append(row[0])
	target_bipgs.append(row[2])
	fam_inst.append(row[3] == "Yes")
	fam_formulae.append(row[4])

# Get shared parameters
app = __revit__.Application

fam_defs  = []
fam_bipgs = []

# Get all definitions and names
spFile   = app.OpenSharedParameterFile()
spGroups = spFile.Groups

sp_defs, sp_nams = [],[]

for g in spGroups:
	for d in g.Definitions:
		sp_defs.append(d)
		sp_nams.append(d.Name)

# Get target parameter definitions
for t in targets_params:
	if t in sp_nams:
		ind = sp_nams.index(t)
		fam_defs.append(sp_defs[ind])

# Catch if we don't have all parameters
if len(fam_defs) != len(targets_params):
	forms.alert("Some parameters not found, refer to report for details.", title="Script cancelled")
	# Show what was missing...
	print("NOT FOUND IN SHARED PARAMETERS FILE:")
	print("---")
	for t in targets_params:
		if t not in sp_nams:
			print(t)
	script.exit()

# Import enum
import System
from System import Enum

# Get all bipgs for checking
bipgs = [a for a in System.Enum.GetValues(DB.BuiltInParameterGroup)]
bipg_names = [str(a) for a in bipgs]

for t in target_bipgs:
	if t in bipg_names:
		ind = bipg_names.index(t)
		fam_bipgs.append(bipgs[ind])

# Catch if we don't have all BIPG's
if len(fam_bipgs) != len(target_bipgs):
	forms.alert("Some groups not found, refer to report for details.", title="Script cancelled")
	# Show what was missing...
	print("NOT A VALID PARAMETER GROUP NAME:")
	print("---")
	for t in target_bipgs:
		if t not in bipg_names:
			print(t)
	script.exit()

# Function to open family document
def famDoc_open(filePath, app):
	try:
		famDoc = app.OpenDocumentFile(filePath)
		return famDoc
	except:
		return None

# Function to close and save family document
def famDoc_close(famDoc, saveOpt=True):
	try:
		famDoc.Close(saveOpt)
		return 1
	except:
		return 0

# Functions to add parameters
from Autodesk.Revit.DB import Transaction

def famDoc_addSharedParams(famDoc, famDefs, famBipgs, famInst, famForm = None):
	# Make sure document is a family document
	if famDoc.IsFamilyDocument:
		# Get family manager and parameter names
		famMan   = famDoc.FamilyManager
		parNames = [p.Definition.Name for p in famMan.Parameters]
		# Make a transaction
		t = Transaction(famDoc, 'Add parameters')
		t.Start()
		# Add parameters to document
		params = []
		for d,b,i,f in zip(famDefs, famBipgs, famInst, famForm):
			if d.Name not in parNames:
				p = famMan.AddParameter(d,b,i)
				params.append(p)
				# Optional, set formulae
				if f != None:
					try:
						famMan.SetFormula(p, f)
					except:
						pass
			else:
				pass
		# Commit transaction
		t.Commit()
		# Return parameters
		return params
	# If not a family document, return None
	else:
		return None

# Finally undertake the process
with forms.ProgressBar(step=1, title="Updating families", cancellable=True) as pb:
	# Create progress bar
	pbCount = 1
	pbTotal = len(path_rfas)
	passCount = 0
	# Run the process
	for filePath in path_rfas:
		# Make sure not cancelled
		if pb.cancelled:
			break
		else:
			famDoc = famDoc_open(filePath, app)
			if famDoc != None:
				pars = famDoc_addSharedParams(famDoc, fam_defs, fam_bipgs, fam_inst, fam_formulae)
				if pb.cancelled or len(pars) == 0:
					famDoc_close(famDoc, False)
				else:
					famDoc_close(famDoc)
					passCount += 1
			# Update progress bar
			pb.update_progress(pbCount, pbTotal)
			pbCount += 1

# Final message to user
form_message = str(passCount) + "/" + str(pbTotal) + " families updated."
forms.alert(form_message, title= "Script completed", warn_icon=False)