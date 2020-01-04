import os

KNACK_CREDENTIALS = {
    "app_id": os.environ.get("knack_app_id", ""),
    "api_key": os.environ.get("knack_app_key", ""),
}