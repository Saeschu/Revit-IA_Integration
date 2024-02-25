def SetNewParameterToCategory(app, doc, spFile,BuiltInCategory, paramterGroupName, parameter_name, paramter_DataType, tooltip):
 
    # Get the BindingMap of the current document
    binding_map = doc.ParameterBindings
    
    
    # Create a category set and insert the category into it
    my_categories = app.Create.NewCategorySet()

    # Use BuiltInCategory to get the category of wall  #ggf. hier ohne get Categorie da beriets eine built in Categorie uebergen wird.
    my_category = Category.GetCategory(doc, BuiltInCategory) 
    my_categories.Insert(my_category)

    #Check if a ParameterBindung of paramter_name already Exist
    iterator = binding_map.ForwardIterator()
    ExistParamterBindung = False
    while (iterator.MoveNext()):

        if iterator.Key.Name == parameter_name:

            CategorySet = iterator.Current.Categories
            ExistParamterBindung = CategorySet.Contains(my_category)

    print(parameter_name, ExistParamterBindung)
    
    if ExistParamterBindung == False:
        print(" Paramter will be added to Category")

    
        # Create a new group in the shared parameters file if not allready exist

        my_groups = spFile.Groups
    
        all_groups = {}
        for group in my_groups:
            all_groups[group.Name] = group


        if paramterGroupName not in all_groups:
            my_group = my_groups.Create(paramterGroupName)
            print("     Group created:  ", my_group.Name)

        else:
            my_group = all_groups[paramterGroupName]
            print("     Group alread exist: ", my_group.Name)      


        # Create an instance definition of the Parameter in definition group MyParameters

        all_paramters ={}
        for parameter in my_group.Definitions:
            all_paramters[parameter.Name] = parameter

        if parameter_name  not in all_paramters:

            option = ExternalDefinitionCreationOptions(parameter_name, paramter_DataType)
            
            # Set tooltip
            option.Description = tooltip
        
            my_definition_product_date = my_group.Definitions.Create(option)
            print("     Parameter created:  ", parameter_name)


        else:
            my_definition_product_date = all_paramters[parameter_name]
            print("     Parameter allready exist:   ", parameter_name)



        # Create an instance of InstanceBinding for the Parameter
        instance_binding = app.Create.NewInstanceBinding(my_categories)
        print("     instance_binding Created:   ", instance_binding)

    
        # Bind the definitions to the document
        instance_bind_ok = binding_map.Insert(my_definition_product_date,
                                            instance_binding, BuiltInParameterGroup.PG_IFC)
        
        print("     instance_bind_ok binded to the document:   ", instance_bind_ok)
        
        return instance_bind_ok