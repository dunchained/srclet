import os, json, pandas
from variables import var
#import var
cwd = os.path.curdir

def read_project_data(project_path):
    file_to_read = open(os.path.join(cwd + var.projects_folder + project_path + '/data.json'))
    file_data = json.load(file_to_read)
    
    data_to_read = pandas.read_excel(os.path.join(cwd + var.projects_folder + project_path + '/data.xlsx'), sheet_name='data_input', skiprows=1)
    data_to_read = data_to_read.drop(data_to_read.columns[0], axis=1)
    column_names = data_to_read.columns.values.tolist()
    
    print(column_names)
    return file_data

def read_methods_data():
    pass