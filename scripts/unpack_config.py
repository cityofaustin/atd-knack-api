"""
Download config.json from S3 and write yaml file. This makes it easier to edit the file.
"""
import json
from pprint import pprint as print
import yaml

import boto3

ENV = "dev"  # `dev` or `production`
BUCKET = "atd-knack-api"  #
FNAME_JSON = "config.json"
FNAME_YAML = "config.yml"
ENVS = ["production", "dev"]
AWS_KEY = "aws_environment_variables"
CONFIG_KEY = "knack_app_config"


def get_config(env, bucket, filename):
    s3 = boto3.resource("s3")
    obj = s3.Object(bucket, filename)
    config = obj.get()["Body"].read()
    return json.loads(config)

config = get_config(ENV, BUCKET, FNAME_JSON)

for env in config.keys():
    config[env][AWS_KEY][CONFIG_KEY] = json.loads(config[env][AWS_KEY][CONFIG_KEY])
    
with open(FNAME_YAML, "w") as fout:
    fout.write(yaml.dump(config))