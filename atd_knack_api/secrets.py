import os
import json

KNACK_CREDENTIALS = json.loads(os.environ.get("knack_app_config", "{}"))
