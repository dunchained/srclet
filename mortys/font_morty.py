import os, json
from variables import var
cwd = os.path.curdir
cwf = os.path.join(cwd + var.settings_folder + var.settings_file)


def read_menu_font_size():
    settings = open(cwf)
    settings_data = json.load(settings)
    settings.close()
    return int(settings_data['menu_font_size'])

#mport os, json
#cwd = os.path.curdir

#settings_folder = '/srclet/settings/'
#settings_file = 'settings.json'

#def read_fonts():
    #settings = open(os.path.join(cwd + settings_folder + settings_file))
    #settings_data = json.load(settings)
    #settings.close()
    #return int(settings_data['menu_font_size'])

#def update_fonts(menu_font_size):
    #settings = open(os.path.join(cwd + settings_folder + settings_file))
    #settings_data = json.load(settings)
    #update = {'menu_font_size': menu_font_size}
    #settings_data.update(update)
    #settings.close()
    #with open(os.path.curdir + settings_folder + settings_file, "w") as outfile:
    #        json.dump(settings_data, outfile)

#update_fonts(14)