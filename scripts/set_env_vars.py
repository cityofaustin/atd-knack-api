"""
For local development. Fetch API credentials from S3 and set knack_app_config env variable.
"""
import json
import os
import boto3

# script configuration
ENV = "dev"  # `dev` or `production`
BUCKET = "atd-knack-api"  #
FILENAME = "config.json"

def load_credentials(env, bucket, filename):
    s3 = boto3.resource("s3")
    obj = s3.Object(bucket, filename)
    config_raw = obj.get()["Body"].read()
    os.environ["knack_app_config"] = json.loads(config_raw).get(env).get("aws_environment_variables").get("knack_app_config")
    return True

if not os.getenv("knack_app_config"):
    load_credentials(ENV, BUCKET, FILENAME)

    if os.getenv("knack_app_config"):
        print("*** Credentials Loaded ***")
    else:
        raise Exception("Failed to load credentials from S3")