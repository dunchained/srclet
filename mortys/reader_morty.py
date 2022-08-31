import os, json
from tkinter import font
from xxlimited import foo
from variables import var
from mortys.language_morty import read_language
from mortys.font_morty import read_menu_font_size, read_text_font_size, read_input_font_size
cwd = os.path.curdir
cwf = os.path.join(cwd + var.settings_folder + var.settings_file)

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

def read_font_size_key(font_size_text):
    language = read_language()
    font_sizes_file = open(os.path.join(cwd + var.language_folder + language + '/' + var.font_sizes_file))
    font_sizes_file_data = json.load(font_sizes_file)
    font_sizes_list = []
    for font_size in font_sizes_file_data:
        font_sizes_list.append(font_sizes_file_data[font_size])
    font_size_key = list(font_sizes_file_data.keys())[list(font_sizes_file_data.values()).index(font_size_text)]
    return font_size_key

def load_json_data_and_check(font_size):
    selected_language = read_language()
    font_sizes_file = cwd + var.language_folder + selected_language + '/' + var.font_sizes_file
    font_sizes = open(font_sizes_file)
    font_sizes_data = json.load(font_sizes)
    if font_size == var.font_size_small:
        font_size_text_to_combo = font_sizes_data['small']
    elif font_size == var.font_size_medium:
        font_size_text_to_combo = font_sizes_data['medium']
    elif font_size == var.font_size_large:
        font_size_text_to_combo = font_sizes_data['large']
    else:
        pass 

    return font_size_text_to_combo

def read_menu_font_size_current_text():
    return load_json_data_and_check(font_size=read_menu_font_size())
    
def read_text_font_size_current_text():
    return load_json_data_and_check(font_size=read_text_font_size())

def read_input_font_size_current_text():
    return load_json_data_and_check(font_size=read_input_font_size())