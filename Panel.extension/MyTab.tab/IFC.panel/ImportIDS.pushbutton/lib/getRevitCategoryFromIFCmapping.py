def getRevitCategoryFromIFCmapping(IfcEntity, IfcCategoryMappingFile):
    print(f'in fuciton: {IfcEntity}')
    RevitCategoryList = []
    
    for row in IfcCategoryMappingFile:
        
        if row.startswith('#') != True:
            item = row.split('\t')

            if str(item[2]).upper().encode('utf-8') == str(IfcEntity).upper().encode('utf-8'):
                print()
                print(f'RevitMappingfile: {str(item[2]).upper().encode("utf-8")}')
                print(f'Entitaet aus IDS: {str(IfcEntity).upper().encode("utf-8")}')
                print(f'Revitkategorie: {str(item[0])}  {item[1]}')

                if item[1] == '':
                    RevitCategory = str(item[0])

                else:
                    RevitCategory = str(item[0] + '\t' + item[1])
                    
                
                RevitCategoryList.append(RevitCategory)
            # else:
            #     RevitCategory = 'kein passende Revit Category gefunden'   

    return RevitCategoryList
