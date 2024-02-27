def getRevitCategoryFromIFCmapping(IfcEntity, IfcCategoryMappingFile):
    RevitCategoryList = []
    
    for row in IfcCategoryMappingFile:

        if row.startswith('#') != True:
            item = row.split('\t')
            print(str(IfcEntity).upper())
            print(str(item[2]).upper())
            if str(item[2]).upper().encode('utf-8') == str(IfcEntity).upper().encode('utf-8'):
                print(item[2])
                # if item[0] not in CategoryList:
                if item[1] == '':
                    RevitCategory = str(item[0])

                else:
                    RevitCategory = str(item[0] + '\t' + item[1])
                    
                
                RevitCategoryList.append(RevitCategory)
            # else:
            #     RevitCategory = 'kein passende Revit Category gefunden'   

    return RevitCategoryList
