import os, json
from variables import var
cwd = os.path.curdir
cwf = os.path.join(cwd + var.settings_folder + var.settings_file)


def read_language():
    settings = open(cwf)
    settings_data = json.load(settings)
    settings.close()
    return settings_data['language']

def language():
    selected_language = read_language()
    language_file = cwd + var.language_folder + selected_language + '/' + selected_language + '.json'
    selected_language_file = open(language_file)
    language = json.load(selected_language_file)
    selected_language_file.close()
    return language

def update_language(new_language):
    settings = open(cwf)
    settings_data = json.load(settings)
    update = {'language': new_language}
    settings_data.update(update)
    settings.close()
    with open(cwf, "w") as outfile:
            json.dump(settings_data, outfile)