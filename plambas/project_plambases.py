import os
import json
import pandas
#
from variables import var
cwd = os.path.curdir
cwd_other = os.path.curdir + var.other_methods_folder


def other_read_methods_data():
    get_files_eto = next(
        os.walk(cwd + var.other_methods_folder), (None, None, []))[2]
    methods_list = []
    methods_parameters = []
    for file in get_files_eto:
        file_to_read = open(os.path.join(
            cwd + var.other_methods_folder + file))
        file_data = json.load(file_to_read)
        if not file_data['complex_parameters']:
            methods_list.append(file_data['symbol'])
            methods_parameters.append(file_data['basic_parameters'])
    res = dict(zip(methods_list, methods_parameters))
    return methods_list, res


def eto_read_methods_data():
    get_files_eto = next(
        os.walk(cwd + var.eto_methods_folder), (None, None, []))[2]
    methods_list = []
    methods_parameters = []
    for file in get_files_eto:
        file_to_read = open(os.path.join(cwd + var.eto_methods_folder + file))
        file_data = json.load(file_to_read)
        methods_list.append(file_data['symbol'])
        if file_data['other_methods']:
            to_append = file_data['basic_parameters'] + \
                ', ' + file_data['other_methods']
        else:
            to_append = file_data['basic_parameters']
        methods_parameters.append(to_append)
    res = dict(zip(methods_list, methods_parameters))
    return methods_list, res


def wb_read_methods_data():
    get_files_eto = next(
        os.walk(cwd + var.wb_methods_folder), (None, None, []))[2]
    methods_list = []
    methods_parameters = []
    for file in get_files_eto:
        file_to_read = open(os.path.join(cwd + var.wb_methods_folder + file))
        file_data = json.load(file_to_read)
        methods_list.append(file_data['symbol'])
        to_append = file_data['basic_parameters']
        if file_data['other_methods']:
            to_append = to_append + ', ' + file_data['other_methods']
        if file_data['eto_methods']:
            to_append = to_append + ', ' + file_data['eto_methods']

        methods_parameters.append(to_append)
    res = dict(zip(methods_list, methods_parameters))
    return methods_list, res


def other_read_methods_data_on_update():
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
        if file_data['complex_parameters']:
            methods_parameters_data = methods_parameters_data + \
                ', ' + file_data['complex_parameters']
        methods_parameters.append(methods_parameters_data)
    res = dict(zip(methods_list, methods_parameters))
    return methods_list, res


def read_project_data(project_path):
    file_to_read = open(os.path.join(
        cwd + var.projects_folder + project_path + '/data.json'))
    file_data = json.load(file_to_read)
    data_to_read = pandas.read_excel(os.path.join(
        cwd + var.projects_folder + project_path + '/data.xlsx'), sheet_name='data_input', skiprows=1)
    # data_to_read = data_to_read.drop(data_to_read.columns[0], axis=1)
    column_names_list = data_to_read.columns.values.tolist()
    column_symbols = []
    for symbol in column_names_list:
        get_files_parameters = next(
            os.walk(cwd + var.basic_parameters_folder), (None, None, []))[2]
        for file1 in get_files_parameters:
            file_to_read1 = open(os.path.join(
                cwd + var.basic_parameters_folder + file1))
            file_data1 = json.load(file_to_read1)
            if symbol == file_data1['name']:
                column_symbols.append(file_data1['symbol'])
    return file_data, column_names_list, column_symbols


def available_changable_parameters(project_path):
    get_files = next(
        os.walk(cwd + var.changable_parameters_folder), (None, None, []))[2]
    cp_list = []
    for file in get_files:
        file_to_read = open(os.path.join(
            cwd + var.changable_parameters_folder + file))
        file_data = json.load(file_to_read)
        acp_dict = {
            "name": file_data['name'],
            "symbol": file_data['symbol'],
            "value": file_data['value']}
        cp_list.append(acp_dict)

    all_data_from_project_dict, _, _ = read_project_data(
        project_path=project_path)
    for key, value in all_data_from_project_dict.items():
        if key == 'weather_station_latitude':
            acp_dict = {"name": 'Wather station latitude',
                        "symbol": key, "value": value}
            cp_list.append(acp_dict)
        elif key == 'weather_station_elevation':
            acp_dict = {"name": 'Wather station elevation',
                        "symbol": key, "value": value}
            cp_list.append(acp_dict)
        elif key == 'weather_station_longitude':
            acp_dict = {"name": 'Wather station longitude',
                        "symbol": key, "value": value}
            cp_list.append(acp_dict)
        else:
            pass
    for_available_parameters = []
    for item in cp_list:
        for_available_parameters.append(item['symbol'])
    return cp_list, for_available_parameters

def read_methods_data():
    # ETO
    get_files_eto = next(
        os.walk(cwd + var.eto_methods_folder), (None, None, []))[2]
    methods_eto_list = []
    for file in get_files_eto:
        file_to_read = open(os.path.join(cwd + var.eto_methods_folder + file))
        file_data = json.load(file_to_read)
        methods_eto_list.append(file_data['name'])

    return methods_eto_list

def read_bp(bpc):
    get_files = next(
        os.walk(cwd + var.basic_parameters_folder), (None, None, []))[2]
    bp_names_list = []
    for bp in bpc:
        for file in get_files:
            file_to_read = open(os.path.join(
                cwd + var.basic_parameters_folder + file))
            file_data = json.load(file_to_read)
            if file_data['symbol'] == bp:
                bp_names_list.append(file_data['name'])
    return bp_names_list


def read_cp(cpc):
    get_files = next(
        os.walk(cwd + var.complex_parameters_folder), (None, None, []))[2]
    cp_names_list = []
    for cp in cpc:
        for file in get_files:
            file_to_read = open(os.path.join(
                cwd + var.complex_parameters_folder + file))
            file_data = json.load(file_to_read)
            if file_data['symbol'] == cp:
                cp_names_list.append(file_data['basic_parameters'])
    return cp_names_list