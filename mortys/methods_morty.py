import os, json, random
cwd = os.path.curdir

categories_file = 'parameter_types.json'
language_folder = '/srclet/languages/'
basic_parameters_folder = '/parameters/basic/'
complex_parameters_folder = '/parameters/changable/'
changable_parameters_folder = '/parameters/changable/'
om_folder = '/methods/others/'
eto_folder = '/methods/eto/'

def read_characters(character_type):
    lista_fajlova = next(os.walk(cwd + character_type), (None, None, []))[2]
    button_list = []
    for file_names in lista_fajlova:
        json_path = os.path.join(cwd + character_type + file_names)
        with open(json_path) as json_file:
                characters = json.load(json_file)
        for key, value in characters.items():
            button_list.append(value)
    columns = 5
    if len(button_list) % 5 == 0:
        rows = len(button_list) // 5
    else:
        rows = len(button_list) // 5 + 1
    return button_list, rows, columns

def read_bp():
    lista_fajlova = next(os.walk(cwd + basic_parameters_folder), (None, None, []))[2]
    button_list = []
    for file_names in lista_fajlova:
        json_path = os.path.join(cwd + basic_parameters_folder + file_names)
        with open(json_path) as json_file:
                characters = json.load(json_file)
                value = characters['symbol']
                button_list.append(value)
    columns = 2
    if len(button_list) % columns == 0:
        rows = len(button_list) // columns
    else:
        rows = len(button_list) // columns + 1
    return button_list, rows, columns

def read_complex_parameters_insert():
    lista_fajlova = next(os.walk(cwd + complex_parameters_folder), (None, None, []))[2]
    button_list = []
    for file_names in lista_fajlova:
        json_path = os.path.join(cwd + complex_parameters_folder + file_names)
        with open(json_path) as json_file:
            characters = json.load(json_file)
            value = characters['symbol']
            if characters['type'] == 'a':
                value = characters['symbol']
                button_list.append(value)
    columns = 3
    if len(button_list) % 3 == 0:
        rows = len(button_list) // 3
    else:
        rows = len(button_list) // 3 + 1
    return button_list, rows, columns

def read_basic_parameters_insert():
    lista_fajlova = next(os.walk(cwd + basic_parameters_folder), (None, None, []))[2]
    button_list = []
    for file_names in lista_fajlova:
        json_path = os.path.join(cwd + basic_parameters_folder + file_names)
        with open(json_path) as json_file:
                characters = json.load(json_file)
                value = characters['symbol']
                button_list.append(value)
    columns = 3
    lista_za_dodati, _, _ = read_complex_parameters()
    button_list = button_list + lista_za_dodati
    
    if len(button_list) % 3 == 0:
        rows = len(button_list) // 3
    else:
        rows = len(button_list) // 3 + 1
    return button_list, rows, columns

def read_complex_parameters():
    lista_fajlova = next(os.walk(cwd + complex_parameters_folder), (None, None, []))[2]
    button_list = []
    for file_names in lista_fajlova:
        json_path = os.path.join(cwd + complex_parameters_folder + file_names)
        with open(json_path) as json_file:
            characters = json.load(json_file)
            value = characters['symbol']
            if characters['type'] == 'a':
                value = characters['symbol']
                button_list.append(value)
    columns = 3
    if len(button_list) % 3 == 0:
        rows = len(button_list) // 3
    else:
        rows = len(button_list) // 3 + 1
    return button_list, rows, columns

def read_cp():
    lista_fajlova = next(os.walk(cwd + changable_parameters_folder), (None, None, []))[2]
    button_list = []
    for file_names in lista_fajlova:
        json_path = os.path.join(cwd + changable_parameters_folder + file_names)
        with open(json_path) as json_file:
            characters = json.load(json_file)
            value = characters['symbol']
            if characters['type'] == 'a':
                value = characters['symbol']
                button_list.append(value)
    columns = 2
    if len(button_list) % columns == 0:
        rows = len(button_list) // columns
    else:
        rows = len(button_list) // columns + 1
    return button_list, rows, columns

def read_om():
    lista_fajlova = next(os.walk(cwd + om_folder), (None, None, []))[2]
    button_list = []
    for file_names in lista_fajlova:
        json_path = os.path.join(cwd + om_folder + file_names)
        with open(json_path) as json_file:
            characters = json.load(json_file)
            value = characters['symbol']
            if characters['type'] == 'a':
                value = characters['symbol']
                button_list.append(value)
    columns = 2
    if len(button_list) % columns == 0:
        rows = len(button_list) // columns
    else:
        rows = len(button_list) // columns + 1
    return button_list, rows, columns

def read_eto():
    lista_fajlova = next(os.walk(cwd + eto_folder), (None, None, []))[2]
    button_list = []
    for file_names in lista_fajlova:
        json_path = os.path.join(cwd + eto_folder + file_names)
        with open(json_path) as json_file:
            characters = json.load(json_file)
            value = characters['symbol']
            if characters['type'] == 'a':
                value = characters['symbol']
                button_list.append(value)
    columns = 2
    if len(button_list) % columns == 0:
        rows = len(button_list) // columns
    else:
        rows = len(button_list) // columns + 1
    return button_list, rows, columns

def read_complex_parameters_non_changable():
    lista_fajlova = next(os.walk(cwd + complex_parameters_folder), (None, None, []))[2]
    button_list = []
    for file_names in lista_fajlova:
        json_path = os.path.join(cwd + complex_parameters_folder + file_names)
        with open(json_path) as json_file:
            characters = json.load(json_file)
            value = characters['symbol']
            if characters['type'] == 'a':
                value = characters['symbol']
                if characters['changable'] == 'no':
                    button_list.append(value)
    columns = 3
    if len(button_list) % 3 == 0:
        rows = len(button_list) // 3
    else:
        rows = len(button_list) // 3 + 1
    return button_list, rows, columns

def get_filename(patameter_type):
    lista = ['q','w','e','r','t','z','u','i','o','p','a','s','d','d','f','g','h','j','k','l','y','x','c','v','b','n','m']
    p = random.choice(lista)
    d = str(random.choice(range(0,9)))
    t = random.choice(lista)
    c = str(random.choice(range(0,9)))
    p2 = random.choice(lista)
    s = str(random.choice(range(0,9)))
    p3 = random.choice(lista)
    d2 = str(random.choice(range(0,9)))
    filename = patameter_type + '_' + p + d + t + c + p2 + s + p3 + d2
    return filename
    