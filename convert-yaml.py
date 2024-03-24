import yaml
import json
import os

# iterate through each YAML file
for filename in os.listdir("yamls"):
    if filename.endswith('.yaml'):
        # open and load the YAML file
        yaml_file =  open("yamls/" + filename)
        loaded_yaml = yaml.safe_load(yaml_file)

        # create/open a JSON file with the same name
        json_file = open("jsons/" + os.path.splitext(filename)[0] + ".json", 'w')

        # convert the YAML contents to JSON
        json.dump(loaded_yaml, json_file)
