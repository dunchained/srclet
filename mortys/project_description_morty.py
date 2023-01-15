import json

def update_project_description(data_file_path, updated_data):
    data_file = open(data_file_path)
    load_data = json.load(data_file)
    update = {
        "project_description": updated_data
        }
    load_data.update(update)
    data_file.close()
    with open(data_file_path, "w") as outfile:
            json.dump(load_data, outfile)