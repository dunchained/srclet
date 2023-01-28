import os, json, pandas
#
import var
cwd = os.path.curdir

def read_project_data(project_path):
    file_to_read = open(os.path.join(cwd + var.projects_folder + project_path + '/data.json'))
    file_data = json.load(file_to_read)
    
    data_to_read = pandas.read_excel(os.path.join(cwd + var.projects_folder + project_path + '/data.xlsx'), sheet_name='data_input', skiprows=1)
    data_to_read = data_to_read.drop(data_to_read.columns[0], axis=1)
    column_names_list = data_to_read.columns.values.tolist()
    return file_data, column_names_list

def read_methods_data(project_path):
    get_files_eto = next(os.walk(cwd + var.eto_methods_folder), (None, None, []))[2]
    for file in get_files_eto:
        file_to_read = open(os.path.join(cwd + var.eto_methods_folder + file))
        file_data = json.load(file_to_read)
        #print(file_data)
        bp1 = file_data['basic_parameters']
        bp = list(bp1.split(', '))

        cp1 = file_data['complex_parameters']
        cp = list(cp1.split(', '))
        cpc = [x for x in cp if x != '']
        
        basic_patameters_list_in_cp = []
        for cepe1 in cpc:
            lista_simbola = []
            get_files_cpc = next(os.walk(cwd + var.complex_parameters_folder), (None, None, []))[2]
            for file in get_files_cpc:
                file_to_read = open(os.path.join(cwd + var.complex_parameters_folder + file))
                file_data = json.load(file_to_read)
                params = file_data['basic_parameters']
                params1 = list(params.split(', '))
            lista_simbola = lista_simbola + params1
            r_parameters = [x for x in lista_simbola if x != '']
            for parameter in r_parameters:
                if parameter not in bp1:
                    bp1 = bp1.append(parameter)
            print(bp1)            
                        
        #     if file_data['symbol'] == 
            # ucitati listu fajlova kompleksnih fajlova i provjeriti i uzeti u 
                        
                #         first_list = [1, 2, 2, 5]
                # second_list = [2, 5, 7, 9]

                # in_first = set(first_list)
                # in_second = set(second_list)

                # in_second_but_not_in_first = in_second - in_first

                # result = first_list + list(in_second_but_not_in_first)
                # print(result)  # Prints [1, 2, 2, 5, 9, 7]

        req_param = bp + cp
        required_parameters = [x for x in req_param if x != '']
        _, available_parameters_list = read_project_data(project_path)
                      
        #req_param = bp + cp
        #required_parameters = [x for x in req_param if x != '']
        
        # required_parametars_names = []
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
