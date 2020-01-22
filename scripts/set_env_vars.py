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

s3 = boto3.resource("s3")
obj = s3.Object(BUCKET, FILENAME)
config_raw = obj.get()["Body"].read()
os.environ["knack_app_config"] = json.loads(config_raw).get(ENV).get("aws_environment_variables").get("knack_app_config")

if os.getenv("knack_app_config"):
    print("*** Credentials Loaded ***")
else:
    raise Exception("Failed to load credentials from S3")