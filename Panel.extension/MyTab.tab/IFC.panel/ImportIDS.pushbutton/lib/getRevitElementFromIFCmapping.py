def getRevitElementFromIFCmapping(Entitylist, IfcCategoryMappingFile):
    mappingDict = {}
    CategoryList =[]

    for row in IfcCategoryMappingFile:
        if row.startswith('#') != True:
            item = row.split('\t')
            print(item)
            if item[2].upper() in Entitylist:
                # if item[0] not in CategoryList:
                if item[1] == '':
                    CategoryList.append(str(item[0]).upper())
                else:
                    CategoryList.append(str(item[0] + '\t' + item[1]).upper())

                mappingDict[str(item[2]).upper()] = CategoryList
                
    return mappingDict