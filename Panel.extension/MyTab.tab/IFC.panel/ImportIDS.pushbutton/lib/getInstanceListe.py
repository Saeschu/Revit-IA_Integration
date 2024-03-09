def getInstanceListe(IfcSchema, EnityName):
    EntityObj = IfcSchema.declaration_by_name(EnityName)
    IsAbstract = EntityObj.is_abstract()
    InstanceListe = []

    while IsAbstract:
        for ChiledEntity in ifcopenshell.util.schema.get_subtypes(EntityObj):
            if ChiledEntity.is_abstract() == False:
                InstanceListe.append(str(ChiledEntity).split(' ')[1][:-1])
                # print(ChiledEntity)
            
        IsAbstract = ChiledEntity.is_abstract()
        EntityObj = ChiledEntity

    return InstanceListe