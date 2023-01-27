import os, json
#from variables import var
import var
cwd = os.path.curdir
cwf = os.path.join(cwd + var.settings_folder + var.settings_file)
#
def read_menu_font_size():
    settings = open(cwf)
    settings_data = json.load(settings)
    settings.close()
    return int(settings_data['menu_font_size'])

def read_text_font_size():
    settings = open(cwf)
    settings_data = json.load(settings)
    settings.close()
    return int(settings_data['text_font_size'])

def read_input_font_size():
    settings = open(cwf)
    settings_data = json.load(settings)
    settings.close()
    return int(settings_data['input_text_size'])

def condition_check(font_size):
    if font_size == 'large':
        font_size_to_write = var.font_size_large
    elif font_size == 'medium':
        font_size_to_write = var.font_size_medium
    elif font_size == 'small':
        font_size_to_write = var.font_size_small
    else:
        font_size_to_write = var.font_size_medium
    return font_size_to_write
    
def update_fonts(menu_font_size, text_font_size, input_font_size):
    settings = open(cwf)
    settings_data = json.load(settings)
    update = {
        'menu_font_size': condition_check(menu_font_size),
        'text_font_size': condition_check(text_font_size),
        'input_text_size': condition_check(input_font_size)
        }
    settings_data.update(update)
    settings.close()
    with open(cwf, "w") as outfile:
            json.dump(settings_data, outfile)