import requests
import json
from pprint import pprint

from tinydb import TinyDB, Query


dbjson = "C:\\temp\\bsdd\\db.json"
# Writing to sample.json
with open(dbjson, "w") as outfile:
    outfile.write("")
db = TinyDB(dbjson)
query =Query()

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
def get_classes(domain_namespaceUri):
    url = BASE_URL + f"/api/SearchInDictionary/v1?DictionaryUri={domain_namespaceUri}"
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


def get_classProperties(ChildClass):
    classInfo = get_classInof(ChildClass['uri'])
                
    if "classProperties" not in classInfo:
        print(ChildClass['name'])
    else:
        print(f"Properties of the selected Class {ChildClass['name']} are:")
        
        for classProperty in classInfo["classProperties"]:
            if "predefinedValue" not in classProperty:
                print('     ', classProperty['name'])

            elif "predefinedValue" in classProperty and classProperty['predefinedValue'] != []:
                print('     ', classProperty['name'], " = ", classProperty['predefinedValue'])
    return classInfo

goon = "Ja"


##__main__##
print("Code Started")
while goon == "ja" or goon == "Ja" or goon =="JA":
    # Dictionaries
    dictionaries = get_dictionaries()

    tempDictionaries = {}
    for dictionary in dictionaries['dictionaries']:
        tempDictionaries[str(dictionary['name'] + " " + dictionary['version'])] = dictionary['uri']
        print('Dictionary Name: ', str(dictionary['name'] + " " + dictionary['version']))

    ##############################################################################################
    Selected_Domain = input("Select an Dictionary: ['FM waveware Spital 2.0'] ")
    if Selected_Domain == '':
        Selected_Domain = "FM waveware Spital 2.0"
    # Selected_Domain = "FM waveware Spital 2.0"
    print(f"Selected_Domain = '{Selected_Domain}'")
     ##############################################################################################
    domain_namespaceUri = tempDictionaries[Selected_Domain]


    #Clases of the Domain
    if dictionaries:
        # domain_namespaceUri = 'https://identifier.buildingsmart.org/uri/bs-agri/fruitvegs/1.0.0' #Eingabe erfolgt über wahl der Domain Name => Domain Uri
        dictionary = get_classes(domain_namespaceUri)["dictionary"]
        ClassList= []

        ParentClass = {}

        #Get PartenClasses
        for classItem in dictionary["classes"]:
            # for classItem in classes["classes"]:
            if classItem['classType'] =='Class':
                Class = get_classInof(classItem["uri"])
                
                ClassList.append(Class)
                db.insert(Class)
                    
                if Class != None and 'parentClassReference' not in Class:
                    print(Class['name'])
                    ParentClass[Class['name']] = Class['uri']
                    getParentClass = True
##############################################################################################
    Selected_ParentClass = input("Select an ParentClass: [RoomCommon] ")
    if Selected_ParentClass == '':
        Selected_ParentClass = "RoomCommon"
    # Selected_ParentClass = "RoomCommon"
    print(f"Selected_ParentClass = '{Selected_ParentClass}'")
##############################################################################################
   

    # print(get_classInof(ParentClass[Selected_ParentClass]))
    

    while getParentClass ==  True:

        result = db.search(query.parentClassReference.name == Selected_ParentClass)

        if result != []:

            for ChildClass in result:
                get_classProperties(ChildClass)
                
                # classInfo = get_classInof(ChildClass['uri'])
                
                # if "classProperties" not in classInfo:
                #     print(ChildClass['name'])
                # else:
                #     print(f"Properties of the selected Class {ChildClass['name']} are:")
                    
                #     for classProperty in classInfo["classProperties"]:
                #         if "predefinedValue" not in classProperty:
                #             print('     ', classProperty['name'])

                #         elif "predefinedValue" in classProperty and classProperty['predefinedValue'] != []:
                #             print('     ', classProperty['name'], " = ", classProperty['predefinedValue'])


            Selected_ParentClass = input("Select an ParentClass: ")
            print(f"Selected_ParentClass = '{Selected_ParentClass}'")
        
        else:
            getParentClass = False
            print(f"{Selected_ParentClass} has no child Classes")
            
            result = db.search(query.name == Selected_ParentClass)
            
            if result != []:
                get_classProperties(result[0])


    # Selected_ParentClass = input("Select an Class: ")

    # Class_namespaceUri = ParentClass[Selected_ParentClass]

    # # Class_namespaceUri = "https://identifier.buildingsmart.org/uri/buildingsmart/ifc/4.3/class/IfcSpace"
    
    # classInfo = get_classInof(Class_namespaceUri)
    # for property in classInfo["classProperties"]:
    #     print(property['propertySet'], ': ', property["name"], '= ', property["predefinedValue"])

    goon = input("Erneute Abfrage starten (Ja | Nein): ")




print("Ende of Code")



                    
  