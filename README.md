# atd-knack-api

A Knack integration server powered by Flask.

## Get It Running

*Requires Python v3.6+*

### Install Requirements

```bash
$ pip install -r requirements.txt
```

### Fix Module Imports and Set Envirnomental Variables

To run the API locally, you'll need enable the `_setpath` helper, which fixes Python module imports when running locally.

In each of these files, find the import statement for `_setpath` near the top of the file, and uncomment it:

- `api.py`
- `_inventory.py`
- `_models.py`

You'll also need to enable the helper script which fetches API credentials from AWS, and loads them as environmental variables. in `api.py`, uncomment the module import for `from scripts import set_env_vars`.

## Deployment

The API is deployed to AWS Lambda with CircleCI. The production branch is automatically pushed to `knack-api.austinmobility.io/`. All other branches are pushed to the staging endpoint.

### Credentials Management

API credentials are stored in `config.json` on AWS S3. 

The configuration file follows this structure:

```json
{
  "dev": {
    "aws_environment_variables": {
      "knack_app_config": "{secret-knack-json}"
    }
  },
  "production": {
    "aws_environment_variables": {
      "knack_app_config": "{secret-knack-json}}"
    }
  }
}
```

The `secret-knack-json` is a quote and linebreak-escaped JSON string which is loaded into the API server environment and parsed by `api.py`. See `secrets.py` for documentation about the structure of the knack json.

To edit `config.json`, use the helper scripts found the `/scripts` directory:

1. `unpack_config.py`

This script fetches the current configuration file from S3, and writes it to `config.yml`. This allows for easy editing of the configuration file as needed.

2. When you've finished your edits, run `load_config.py`. This will convert `config.yml` to the expected JSON format and upload it to S3.