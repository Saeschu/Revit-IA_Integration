#! python3
#############################################################################
import requests
import json

from Autodesk.Revit.DB import *
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


def get_classProperties(doc, RevitElement, RevitSourceParamter, classInfo_namespaceUri):
    classInfo = get_classInof(classInfo_namespaceUri)
                
    if "classProperties" not in classInfo:
        pass
    else:
        print(f"Properties of the Class {classInfo['name']} are:")
        
        ClassPropertyList = []
        for classProperty in classInfo["classProperties"]:
            if "predefinedValue" not in classProperty:
                print(f'      {classProperty["name"]}')
                
                
              
            # ToDo Umbauen in Dic innerhalb feld Classxy
            elif "predefinedValue" in classProperty and classProperty['predefinedValue'] != []:
                ClassPropertyList.append(str(classProperty["name"] + '\n'))
                print(f'      {classProperty["name"]}  =  {classProperty["predefinedValue"]}')
                
        RevitParamter = RevitElement.LookupParameter(f'{RevitSourceParamter} Description')
        print(f'Paramtername: {RevitSourceParamter} Description')
        print(f'ParameterValue: {ClassPropertyList}')

        t = Transaction(doc, "Ergaenze Classification Parameter")
        t.Start()
        # classProperty["predefinedValue"])
        RevitParamter.Set(ClassPropertyList)
        
        t.Commit()

    return True




##__main__##

def getbSDDRequest(doc, RevitElement, Selected_Dictionary, Selected_Class):
  
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
    
    RevitSourceParamter = "ClassifiacationCode"
    classProperties = get_classProperties(doc,RevitElement, RevitSourceParamter, classInfo['uri'])

    return classProperties
    
# print(get_dictionaries())
# getbSDDRequest("FM waveware Spital", "Büro")
