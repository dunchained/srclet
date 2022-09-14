import os, json
from variables import var
cwd = os.path.curdir
cwf = os.path.join(cwd + var.settings_folder + var.settings_file)
#

def icon_size():
    settings = open(cwf)
    settings_data = json.load(settings)
    settings.close()
    return int(settings_data['icon_size'])