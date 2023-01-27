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
        bp = list(file_data['basic_parameters'].split(', '))
        
        file_datafile_data['basic_parameters'].
        + ', ' + file_data['complex_parameters']
        required_parameters = file_data['basic_parameters'] + ', ' + file_data['complex_parameters']
        _, available_parameters_list = read_project_data(project_path)
        check = all(item in required_parameters for item in available_parameters_list)
        if check:
            print(required_parameters, available_parameters_list)
            print("The list1 contains all elements of the list2", file_data['name'])
        else:
            print("No, List1 doesn't have all elements of the List2.", file_data['name'])
            print(required_parameters, available_parameters_list)