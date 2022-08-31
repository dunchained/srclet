import os, json
from variables import var
from mortys.language_morty import read_language
cwd = os.path.curdir

def read_font_size_text():
    selected_language = read_language()
    font_sizes_file = cwd + var.language_folder + selected_language + '/' + var.font_sizes_file
    font_sizes = open(font_sizes_file)
    font_sizes_data = json.load(font_sizes)
    font_sizes_list = []
    for key, value in font_sizes_data.items():
        font_sizes_list.append(value)
    font_sizes.close()
    return font_sizes_list