import os, json, pandas
import var
cwd = os.path.curdir
cwd_other = os.path.curdir + var.other_methods_folder

def read_project_data(project_path):
    file_to_read = open(os.path.join(cwd + var.projects_folder + project_path + '/data.json'))
    file_data = json.load(file_to_read)
    data_to_read = pandas.read_excel(os.path.join(cwd + var.projects_folder + project_path + '/data.xlsx'), sheet_name='data_input', skiprows=1)
    column_names_list = data_to_read.columns.values.tolist()
    
    column_symbols = []
    get_files_bp = next(os.walk(cwd + var.basic_parameters_folder), (None, None, []))[2]
    for name_bp in column_names_list:
        for file_bp in get_files_bp:
            file_to_read_bp = open(os.path.join(cwd + var.basic_parameters_folder + file_bp))
            file_data_bp = json.load(file_to_read_bp)
            if name_bp.strip() == file_data_bp['name'].strip():
                column_symbols.append(file_data_bp['symbol'])

    get_files_om = next(os.walk(cwd + var.other_methods_folder), (None, None, []))[2]
    for name_om in column_names_list:
        for file_om in get_files_om:
            file_to_read_om = open(os.path.join(cwd + var.other_methods_folder + file_om))
            file_data_om = json.load(file_to_read_om)
            if name_om.strip() == file_data_om['name'].strip():
                column_symbols.append(file_data_om['symbol'])
    
    get_files_eto = next(os.walk(cwd + var.eto_methods_folder), (None, None, []))[2]
    for name_eto in column_names_list:
        for file_eto in get_files_eto:
            file_to_read_eto = open(os.path.join(cwd + var.eto_methods_folder + file_eto))
            file_data_eto = json.load(file_to_read_eto)
            if name_eto.strip() == file_data_eto['name'].strip():
                column_symbols.append(file_data_eto['symbol'])
    return file_data, column_names_list, column_symbols

def read_cps(project_path):
    get_files = next(os.walk(cwd + var.changable_parameters_folder), (None, None, []))[2]
    cp_list = []
    for file in get_files:
        file_to_read = open(os.path.join(cwd + var.changable_parameters_folder + file))
        file_data = json.load(file_to_read)
        acp_dict = {
            "name": file_data['name'],
            "symbol": file_data['symbol'],
            "value": file_data['value']}
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
        if file_data['changable_parameters']:
            methods_parameters_data = methods_parameters_data + \
                ', ' + file_data['changable_parameters']
        methods_parameters.append(methods_parameters_data)
    res = dict(zip(methods_list, methods_parameters))
    return methods_list, res



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