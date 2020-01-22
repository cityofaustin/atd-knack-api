"""
Write config.json to yaml file. This makes it easier to edit the file.
"""
import json
from pprint import pprint as print
import yaml
import pdb

FNAME_JSON = "config.json"
FNAME_YAML = "config.yml"

ENVS = ["production", "dev"]
AWS_KEY = "aws_environment_variables"
CONFIG_KEY = "knack_app_config"

with open(FNAME_JSON, "r") as fin:
    config = json.loads(fin.read())

for env in config.keys():
    config[env][AWS_KEY][CONFIG_KEY] = json.loads(config[env][AWS_KEY][CONFIG_KEY])
    
with open(FNAME_YAML, "w") as fout:
    fout.write(yaml.dump(config))