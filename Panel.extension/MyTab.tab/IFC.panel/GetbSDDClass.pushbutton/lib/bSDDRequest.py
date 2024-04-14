#! python3
#############################################################################
import requests
import json

# from Autodesk.Revit.DB import *
##############################################################################


BASE_URL = 'https://api.bsdd.buildingsmart.org/'

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
        # print(response.text)
        return None

def get_classInof(class_namespaceUri):
    url = BASE_URL + f"/api//Class/v1?uri={class_namespaceUri}&includeClassProperties=true&includeChildClassReferences=true&includeClassRelations=true"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(response.text)
        return None


def get_classProperties(classInfo_namespaceUri):
    classInfo = get_classInof(classInfo_namespaceUri)
    ClassPropertyList = []

    if "classProperties" not in classInfo:
        print(f'- {classInfo["name"]}')
        pass
    else:
        print(f"\nProperties der Class {classInfo['name']} sind:")
        
        
        for classProperty in classInfo["classProperties"]:
            if "predefinedValue" not in classProperty:
                print(f'      {classProperty["name"]}')
                
            elif "predefinedValue" in classProperty and classProperty['predefinedValue'] != []:
                ClassPropertyList.append(f'{classProperty["name"]} : {classProperty["predefinedValue"]}\n')

                print(f'-      {classProperty["name"]}  =  {classProperty["predefinedValue"]}') 

    return classInfo, ClassPropertyList




##__main__##

def getbSDDRequest(Selected_Dictionary, Selected_Class):
  
    ## Dictionaries
    dictionaries = get_dictionaries()

    selectionDic = {}
    for dictionary in dictionaries['dictionaries']:
        if dictionary['name'] == str(Selected_Dictionary):
            selectionDic[str(dictionary['name'])] = dictionary['uri']
            selectionDic['oriDict'] = dictionary

            break

    
    bsddClasses = get_classes(selectionDic[Selected_Dictionary])
    
    selectionClass = {}
    for bsddClass in bsddClasses['dictionary']['classes']:
        if bsddClass['name'] == Selected_Class:

            selectionClass[str(bsddClass['name'])] = bsddClass['uri']
            selectionClass['oriDict'] = bsddClass
            

    classInfo = get_classInof(selectionClass[Selected_Class])
    
    classProperties = get_classProperties(classInfo['uri'])[1]

    return classProperties
    
# print(get_dictionaries())
# getbSDDRequest("FM waveware Spital", "Büro")

