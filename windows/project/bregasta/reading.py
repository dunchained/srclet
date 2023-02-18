import os, json, pandas
#
import var
cwd = os.path.curdir

def read_project_data_file(project_path):
    file_to_read = open(os.path.join(project_path + '/data.json'))
    file_data_list = json.load(file_to_read)
    data_to_read = pandas.read_excel(os.path.join(project_path + '/data.xlsx'), sheet_name='data_input', skiprows=1)
    #data_to_read = data_to_read.drop(data_to_read.columns[0], axis=1)
    column_names_list = data_to_read.columns.values.tolist()
    return file_data_list, column_names_list