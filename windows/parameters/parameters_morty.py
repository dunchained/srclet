import os, json, random
cwd = os.path.curdir

categories_file = 'parameter_types.json'
language_folder = '/srclet/languages/'

def read_characters(character_type):
    lista_fajlova = next(os.walk(cwd + character_type), (None, None, []))[2]
    print(character_type)
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
    