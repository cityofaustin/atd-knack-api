"""
Translate config.yml to json and upload to S3.

The output json matches the structure expected by
the .circleci deployment script, including the quote-escaped API keys JSON, which 
which are loaded into the API environment vars.
"""
import json
from pprint import pprint as print
import yaml
import pdb

import boto3

BUCKET = "atd-knack-api"  #
FNAME_JSON = "config.json"
FNAME_YAML = "config.yml"
ENVS = ["production", "dev"]
AWS_KEY = "aws_environment_variables"
CONFIG_KEY = "knack_app_config"

with open(FNAME_YAML, "r") as fin:
    config = yaml.load(fin.read())

for env in config.keys():
    config_json = json.dumps(config[env][AWS_KEY][CONFIG_KEY])
    config[env][AWS_KEY][CONFIG_KEY] = config_json

with open(FNAME_JSON, "w") as fout:
    fout.write(json.dumps(config))

s3 = boto3.resource('s3')
s3.Object(BUCKET, FNAME_JSON).upload_file(Filename=FNAME_JSON)