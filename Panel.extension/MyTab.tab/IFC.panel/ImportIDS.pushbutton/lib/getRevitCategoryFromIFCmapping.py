def getRevitCategoryFromIFCmapping(IfcEntity, IfcCategoryMappingFile):
    
    RevitCategory = 'kein passende Revit Category gefunden'
    for row in IfcCategoryMappingFile:
        if row.startswith('#') != True:
            item = row.split('\t')

            if str(item[2]).upper() == str(IfcEntity).upper():
                # if item[0] not in CategoryList:
                if item[1] == '':
                    RevitCategory = str(item[0])
                    break
                    
                else:
                    RevitCategory = str(item[0] + '\t' + item[1])
                    break
                
            # else:
            #     RevitCategory = 'kein passende Revit Category gefunden'   


    return RevitCategory
