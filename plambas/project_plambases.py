import os, json
from pathlib import Path
from variables import var
cwd = os.path.curdir
cwd_other = os.path.curdir + var.other_methods_folder


def other_read_methods_data():
    get_files_eto = next(
        os.walk(cwd + var.other_methods_folder), (None, None, []))[2]
    methods_list = []
    methods_parameters = []
    for file in get_files_eto:
        file_data = json.loads(Path(cwd + var.other_methods_folder + file).read_text(encoding="utf-8"))
        if not file_data['changable_parameters']:
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
        file_data = json.loads(Path(cwd + var.eto_methods_folder + file).read_text(encoding="utf-8"))
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
        file_data = json.loads(Path(cwd + var.wb_methods_folder + file).read_text(encoding="utf-8"))
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
        file_data = json.loads(Path(cwd + var.other_methods_folder + file).read_text(encoding="utf-8"))
        methods_list.append(file_data['symbol'])
        methods_parameters_data = file_data['basic_parameters']
        if file_data['changable_parameters']:
            methods_parameters_data = methods_parameters_data + \
                ', ' + file_data['changable_parameters']
        methods_parameters.append(methods_parameters_data)
    res = dict(zip(methods_list, methods_parameters))
    return methods_list, res

def read_project_data(project_path):
    from plambas.monthly_data import PROJECTS, catalog, load_project
    path = Path(project_path)
    if not path.is_absolute() and len(path.parts) == 1:
        path = PROJECTS / path
    metadata, columns, _ = load_project(path)
    fields = catalog()
    names = [fields.get(key, (key, ""))[0] for key in columns]
    legacy_ids = {"Month": "M", "Year": "Y"}
    symbols = [legacy_ids.get(key, key) for key in columns]
    return metadata, names, symbols


def available_changable_parameters(project_path):
    get_files = next(
        os.walk(cwd + var.changable_parameters_folder), (None, None, []))[2]
    cp_list = []
    for file in get_files:
        file_data = json.loads(Path(cwd + var.changable_parameters_folder + file).read_text(encoding="utf-8"))
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
                        "symbol": key, "value": str(value)}
            cp_list.append(acp_dict)
        elif key == 'weather_station_elevation':
            acp_dict = {"name": 'Wather station elevation',
                        "symbol": key, "value": str(value)}
            cp_list.append(acp_dict)
        elif key == 'weather_station_longitude':
            acp_dict = {"name": 'Wather station longitude',
                        "symbol": key, "value": str(value)}
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
        file_data = json.loads(Path(cwd + var.eto_methods_folder + file).read_text(encoding="utf-8"))
        methods_eto_list.append(file_data['name'])

    return methods_eto_list

def read_bp(bpc):
    get_files = next(
        os.walk(cwd + var.basic_parameters_folder), (None, None, []))[2]
    bp_names_list = []
    for bp in bpc:
        for file in get_files:
            file_data = json.loads(Path(cwd + var.basic_parameters_folder + file).read_text(encoding="utf-8"))
            if file_data['symbol'] == bp:
                bp_names_list.append(file_data['name'])
    return bp_names_list


def read_cp(cpc):
    get_files = next(
        os.walk(cwd + var.complex_parameters_folder), (None, None, []))[2]
    cp_names_list = []
    for cp in cpc:
        for file in get_files:
            file_data = json.loads(Path(cwd + var.complex_parameters_folder + file).read_text(encoding="utf-8"))
            if file_data['symbol'] == cp:
                cp_names_list.append(file_data['basic_parameters'])
    return cp_names_list