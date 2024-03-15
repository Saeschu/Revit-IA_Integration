#! python3

### SATART of CODE ImportIDS ###
#Autor: Sascha Hostettler
#Datum: 20.05.2024
#Version: ?
#Beschrieb: 
#
#
### SATART of CODE ImportIDS ###
# print('\n### SATART of CODE ImportIDS ###')
##############################################################################
import requests
import json

from pyrevit import EXEC_PARAMS, DB
from Autodesk.Revit.DB import *
import System
from System import Enum

# sys.path.append( '/Pnale.extenstion/lib')
# from mymodule import get_RevitElementFromIFCmapping 

##############################################################################


BASE_URL = 'https://api.bsdd.buildingsmart.org/'

##############################################################################

class Classification():
    def __init__(self, ClassValue):
        self.ClassValue = ClassValue
        self.parseInput()

    def parseInput(self):

        parts = self.ClassValue.strip('[]').split(':')
        self.Class = parts[0].split(']')[0]

        if len(parts[0].split(']')) > 1:
            self.Code = parts[0].split(']')[1]

            if len(parts) > 1:
                self.Title = parts[1]
            else:
                self.Title = None
        else:
            self.Code = None
            self.Title = None

class   ClassificationHandler:
    def __init__(self, RevitElement, SelectedDictionary, SelectedClass):
        self.RevitElement = RevitElement
        self.SelectedDictionary = SelectedDictionary
        self.SelectedClass = SelectedClass
        self.parameterName = None
        self.parameterValue = None
        self.setParamter() 

    def setParamter(self):
        # try:
        getbSDDRequest(self.RevitElement, self.SelectedDictionary, self.SelectedClass)
        # except:
            # print(f'Error occurs while bSDD request, Selected_Dictionary: {self.SelectedDictionary}, Selected_Class: {self.SelectedClass}')

# get a liste of all domains
def get_dictionaries():
    url = BASE_URL + "/api/Dictionary/v1"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(response.text)
        return None

#Choos an Domain an get a list of all Classes
def get_classes(Dictionary_namespaceUri):
    url = BASE_URL + f"/api/SearchInDictionary/v1?DictionaryUri={Dictionary_namespaceUri}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(response.text)
        return None

def get_classInof(class_namespaceUri):
    url = BASE_URL + f"/api//Class/v1?uri={class_namespaceUri}&includeClassProperties=true&includeChildClassReferences=true&includeClassRelations=true"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(response.text)
        return None


def get_classProperties(RevitElement, Selected_Dictionary, classInfo_namespaceUri):
    classInfo = get_classInof(classInfo_namespaceUri)
    if "classProperties" not in classInfo:
        pass
    else:
        print(f"Properties of the Class {classInfo['name']} are:")
        
        for classProperty in classInfo["classProperties"]:
            if "predefinedValue" not in classProperty:
                print(f'      {classProperty["name"]}')
                
            elif "predefinedValue" in classProperty and classProperty['predefinedValue'] != []:
                print(f'      {classProperty["name"]}  =  {classProperty["predefinedValue"]}')
                
                RevitParamter = RevitElement.LookupParameter(f'{Selected_Dictionary}.{classProperty["name"]}')
                print(RevitParamter)
                t = Transaction(doc, "Ergaenze Classification Parameter")
                t.Start()

                RevitParamter.Set(classProperty["predefinedValue"])
                
                t.Commit()
                
    return True

def getbSDDRequest(RevitElement, Selected_Dictionary, Selected_Class):
  
    ## Dictionaries
    dictionaries = get_dictionaries()

    selectionDic = {}
    for dictionary in dictionaries['dictionaries']:
       
        if dictionary['name'] == Selected_Dictionary:
            
            selectionDic[str(dictionary['name'])] = dictionary['uri']
            selectionDic['oriDict'] = dictionary
           
            break

   
    bsddClasses = get_classes(selectionDic[Selected_Dictionary])
    
    selectionClass = {}
    for bsddClass in bsddClasses['dictionary']['classes']:
        if bsddClass['name'] == Selected_Class:

            selectionClass[str(bsddClass['name'])] = bsddClass['uri']
            selectionClass['oriDict'] = bsddClass
            
            break

    classInfo = get_classInof(selectionClass[Selected_Class])

    classProperties = get_classProperties(RevitElement, Selected_Dictionary, classInfo['uri'])

    return classProperties

# ClassValue = Classification(ParameterValue)
# ClassificationHandler(RevitElement, ClassValue.Class, ClassValue.Code)