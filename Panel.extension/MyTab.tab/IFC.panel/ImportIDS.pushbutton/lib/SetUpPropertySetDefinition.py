
import csv

##############################################################################

class IDSPropertySetDefinition():
    def __init__(self, Entity, requ):
        self.Entity = Entity
        self.PropertySetName = requ.propertySet
        self.PropertyName = requ.name
        self.PropertyDataType = 'Text'
        self.RevitParameterName = 'temp'


    def SetTyping(self):
        #Später kann hier unterschieden werden ob Applicalbility auf Predefined Typ oder auf Instanz geht
        if len(str(self.Entity).split('.')) == 1:
            return 'I'
        else:
            return 'T'

    def SetPropertySet(self):
        return ['PropertySet:', self.PropertySetName, self.SetTyping(), self.Entity ]


    def SetProperty(self):
        return ['', self.PropertyName,  self.PropertyDataType,  self.RevitParameterName]

##############################################################################
# __MAIN__


def SetUpIDSPropertySetDefinition(RevitParameterMappingDataFrame, Entity, requ):
   
    definition = IDSPropertySetDefinition(Entity, requ)
    PropertySetList = {}
    PropertyList = {}
    EntityListFromPropertySet = {}

    for line in RevitParameterMappingDataFrame:
        if line[0] == 'PropertySet:':
            PropertySetList[line[1]] = line.index(line[1])
            EntityListFromPropertySet[line[1]] = list(line[2])
        elif line[0] =='':
            PropertyList[line[1]] = line.index(line[1])


    if definition.PropertySetName in PropertySetList.keys() and definition.PropertyName in PropertyList.keys():
        pass

    elif definition.PropertySetName not in PropertySetList.keys() and definition.PropertyName not in PropertyList.keys():
        # print('Status 1: beides neu anlegen')
        RevitParameterMappingDataFrame.append(definition.SetPropertySet())
        RevitParameterMappingDataFrame.append(definition.SetProperty())
        

    elif definition.PropertySetName in PropertySetList.keys() and definition.PropertyName not in PropertyList.keys():
        # print('Status2: Property an bestehendes Pset anlegen')
        RevitParameterMappingDataFrame.insert(PropertySetList[definition.PropertySetName] , definition.SetProperty())

        if definition.Entity not in EntityListFromPropertySet[definition.PropertySetName]:
            EntityList = RevitParameterMappingDataFrame[PropertySetList[definition.PropertySetName]-1][3]
            RevitParameterMappingDataFrame[PropertySetList[definition.PropertySetName]-1][3] = (f'{EntityList}, {definition.Entity}')
    


    elif definition.PropertySetName not in PropertySetList.keys() and definition.PropertyName in PropertyList.keys():
        # print('Property ist bereits in einem PSet gespeichert')
        pass

    
    return RevitParameterMappingDataFrame





