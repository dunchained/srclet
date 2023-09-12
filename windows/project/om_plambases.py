import os, json, pandas
import var
cwd = os.path.curdir

def read_om_data():
    get_files_eto = next(os.walk(cwd + var.other_methods_folder), (None, None, []))[2]
    methods_list = []
    methods_parameters = []
    for file in get_files_eto:
        file_to_read = open(os.path.join(cwd + var.other_methods_folder + file))
        file_data = json.load(file_to_read)
        methods_list.append(file_data['symbol'])
        methods_parameters.append(file_data['basic_parameters'])
        methods_parameters.append(file_data['changable_parameters'])
        methods_parameters.append(file_data['other_methods'])
    res = dict(zip(methods_list, methods_parameters))
    print(methods_list, res)
    return methods_list, res

def read_om_on_update():
    get_files_eto = next(
        os.walk(cwd + var.other_methods_folder), (None, None, []))[2]
    methods_list = []
    methods_parameters = []
    for file in get_files_eto:
        file_to_read = open(os.path.join(
            cwd + var.other_methods_folder + file))
        file_data = json.load(file_to_read)
        methods_list.append(file_data['symbol'])
        methods_parameters_data = file_data['basic_parameters']
        if file_data['changable_parameters']:
            methods_parameters_data = methods_parameters_data + \
                ', ' + file_data['changable_parameters']
        if file_data['other_methods']:
            methods_parameters_data = methods_parameters_data + \
                ', ' + file_data['other_methods']
        methods_parameters.append(methods_parameters_data)
    res = dict(zip(methods_list, methods_parameters))
    return methods_list, res