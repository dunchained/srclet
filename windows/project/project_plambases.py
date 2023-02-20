import os, json, pandas
#
import var
cwd = os.path.curdir
cwd_other = os.path.curdir + var.other_methods_folder

def other_read_methods_data():
    get_files_eto = next(os.walk(cwd + var.other_methods_folder), (None, None, []))[2]
    methods_list = []
    methods_parameters = []
    for file in get_files_eto:
        file_to_read = open(os.path.join(cwd + var.other_methods_folder + file))
        file_data = json.load(file_to_read)
        if not file_data['complex_parameters']:
            methods_list.append(file_data['symbol'])
            methods_parameters.append(file_data['basic_parameters'])
    res = dict(zip(methods_list, methods_parameters))
    return methods_list, res

def eto_read_methods_data():
    get_files_eto = next(os.walk(cwd + var.eto_methods_folder), (None, None, []))[2]
    methods_list = []
    methods_parameters = []
    for file in get_files_eto:
        file_to_read = open(os.path.join(cwd + var.eto_methods_folder + file))
        file_data = json.load(file_to_read)
        methods_list.append(file_data['symbol'])
        if file_data['other_methods']:
            to_append = file_data['basic_parameters'] + ', ' + file_data['other_methods']
        else:
            to_append = file_data['basic_parameters']
        methods_parameters.append(to_append)
    res = dict(zip(methods_list, methods_parameters))
    return methods_list, res

def wb_read_methods_data():
    get_files_eto = next(os.walk(cwd + var.eto_methods_folder), (None, None, []))[2]
    methods_list = []
    methods_parameters = []
    for file in get_files_eto:
        file_to_read = open(os.path.join(cwd + var.eto_methods_folder + file))
        file_data = json.load(file_to_read)
        methods_list.append(file_data['symbol'])
        if file_data['other_methods']:
            to_append = file_data['basic_parameters'] + ', ' + file_data['other_methods']
        else:
            to_append = file_data['basic_parameters']
        methods_parameters.append(to_append)
    res = dict(zip(methods_list, methods_parameters))
    return methods_list, res

def other_read_methods_data_on_update():
    get_files_eto = next(os.walk(cwd + var.other_methods_folder), (None, None, []))[2]
    methods_list = []
    methods_parameters = []
    for file in get_files_eto:
        file_to_read = open(os.path.join(cwd + var.other_methods_folder + file))
        file_data = json.load(file_to_read)
        methods_list.append(file_data['symbol'])
        methods_parameters_data = file_data['basic_parameters']
        if file_data['complex_parameters']:
            methods_parameters_data = methods_parameters_data + ', ' + file_data['complex_parameters']
        methods_parameters.append(methods_parameters_data)
    res = dict(zip(methods_list, methods_parameters))
    return methods_list, res

def read_project_data(project_path):
    file_to_read = open(os.path.join(cwd + var.projects_folder + project_path + '/data.json'))
    file_data = json.load(file_to_read)
    data_to_read = pandas.read_excel(os.path.join(cwd + var.projects_folder + project_path + '/data.xlsx'), sheet_name='data_input', skiprows=1)
    #data_to_read = data_to_read.drop(data_to_read.columns[0], axis=1)
    column_names_list = data_to_read.columns.values.tolist()
    column_symbols = []
    for symbol in column_names_list:
        get_files_parameters = next(os.walk(cwd + var.basic_parameters_folder), (None, None, []))[2]
        for file1 in get_files_parameters:
            file_to_read1 = open(os.path.join(cwd + var.basic_parameters_folder + file1))
            file_data1 = json.load(file_to_read1)
            if symbol == file_data1['name']:
                column_symbols.append(file_data1['symbol'])
    return file_data, column_names_list, column_symbols

def available_changable_parameters(project_path):
    get_files = next(os.walk(cwd + var.changable_parameters_folder), (None, None, []))[2]
    cp_list = []
    for file in get_files:
        file_to_read = open(os.path.join(cwd + var.changable_parameters_folder + file))
        file_data = json.load(file_to_read)
        if file_data['type'] == 'a':
            file_changable = file_data['changable']
            if file_changable == 'yes':
                acp_dict = {"name": file_data['name'], "symbol": file_data['symbol'], "value": file_data['formula']}
                cp_list.append(acp_dict)
    all_data_from_project_dict, _, _ = read_project_data(project_path=project_path)
    for key, value in all_data_from_project_dict.items():
        if key == 'weather_station_latitude':
            acp_dict = {"name": 'Wather station latitude', "symbol": key, "value": value}
            cp_list.append(acp_dict)
        elif key == 'weather_station_elevation':
            acp_dict = {"name": 'Wather station elevation', "symbol": key, "value": value}
            cp_list.append(acp_dict)
        elif key == 'weather_station_longitude':
            acp_dict = {"name": 'Wather station longitude', "symbol": key, "value": value}
            cp_list.append(acp_dict)        
        else:
            pass
    for_available_parameters = []
    for item in cp_list:
        for_available_parameters.append(item['symbol'])
    return cp_list, for_available_parameters

#######################################################################



# def read_project_data(project_path):
#     file_to_read = open(os.path.join(cwd + var.projects_folder + project_path + '/data.json'))
#     file_data = json.load(file_to_read)
#     data_to_read = pandas.read_excel(os.path.join(cwd + var.projects_folder + project_path + '/data.xlsx'), sheet_name='data_input', skiprows=1)
#     #data_to_read = data_to_read.drop(data_to_read.columns[0], axis=1)
#     column_names_list = data_to_read.columns.values.tolist()
#     return file_data, column_names_list

def read_methods_data():
    # ETO
    get_files_eto = next(os.walk(cwd + var.eto_methods_folder), (None, None, []))[2]
    methods_eto_list = []
    for file in get_files_eto:
        file_to_read = open(os.path.join(cwd + var.eto_methods_folder + file))
        file_data = json.load(file_to_read)
        methods_eto_list.append(file_data['name'])
        
    return methods_eto_list

        # bp1 = file_data['basic_parameters']
        # bp = list(bp1.split(', '))
        # bpc = [x for x in bp if x != '']
        
        # bpc_names = read_bp(bpc)
        # #print('BP Lista bez Kompleksnih: ', bpc_names)
        
        # cp1 = file_data['complex_parameters']
        # cp = list(cp1.split(', '))
        # cpc = [x for x in cp if x != '']
        
        # cpc_names = read_cp(cpc)
        # #print('BP Lista u Kompleksnih: ', cpc_names)
        
def read_bp(bpc):
    get_files = next(os.walk(cwd + var.basic_parameters_folder), (None, None, []))[2]
    bp_names_list = []
    for bp in bpc:
        for file in get_files:
            file_to_read = open(os.path.join(cwd + var.basic_parameters_folder + file))
            file_data = json.load(file_to_read)
            if file_data['symbol'] == bp:
                bp_names_list.append(file_data['name'])
    return bp_names_list

def read_cp(cpc):
    get_files = next(os.walk(cwd + var.complex_parameters_folder), (None, None, []))[2]
    cp_names_list = []
    for cp in cpc:
        for file in get_files:
            file_to_read = open(os.path.join(cwd + var.complex_parameters_folder + file))
            file_data = json.load(file_to_read)
            if file_data['symbol'] == cp:
                #print(file_data['basic_parameters'])
                #print(file_data['complex_parameters'])
                cp_names_list.append(file_data['basic_parameters'])
    return cp_names_list
    
        
        # for cepe1 in cpc:
        #     lista_simbola = []
        #     get_files_cpc = next(os.walk(cwd + var.complex_parameters_folder), (None, None, []))[2]
        #     for file in get_files_cpc:
        #         file_to_read = open(os.path.join(cwd + var.complex_parameters_folder + file))
        #         file_data = json.load(file_to_read)
        #         params = file_data['basic_parameters']
        #         params1 = list(params.split(', '))
        #     lista_simbola = lista_simbola + params1
        #     r_parameters = [x for x in lista_simbola if x != '']
        #     for parameter in r_parameters:
        #         if parameter not in bp1:
        #            # bp1 = bp1.append(parameter)
        #     #print(bp1)            
                        
        # #     if file_data['symbol'] == 
        #     # ucitati listu fajlova kompleksnih fajlova i provjeriti i uzeti u 
                        
        #         #         first_list = [1, 2, 2, 5]
        #         # second_list = [2, 5, 7, 9]

        #         # in_first = set(first_list)
        #         # in_second = set(second_list)

                # in_second_but_not_in_first = in_second - in_first

                # result = first_list + list(in_second_but_not_in_first)
                # print(result)  # Prints [1, 2, 2, 5, 9, 7]

        # req_param = bp + cp
        # required_parameters = [x for x in req_param if x != '']
        # _, available_parameters_list = read_project_data(project_path)
                      
        # #req_param = bp + cp
        # #required_parameters = [x for x in req_param if x != '']
        
        # # required_parametars_names = []
        # get_files_basic = next(os.walk(cwd + var.basic_parameters_folder), (None, None, []))[2]
        # for file in get_files_eto:
        #     file_to_read = open(os.path.join(cwd + var.basic_parameters_folder + file))
        #     file_data = json.load(file_to_read)
        #     if file_data['symbol'] == 
        
        # _, available_parameters_list = read_project_data(project_path)
      
        # check = set(required_parameters).issubset(available_parameters_list)
        # if check:
        #     print(required_parameters)
        #     print(available_parameters_list)
        #     print("The list1 contains all elements of the list2", file_data['name'])
        # else:
        #     print(required_parameters)
        #     print(available_parameters_list)
        #     print("No, List1 doesn't have all elements of the List2.", file_data['name'])

