"""
Check Data Tracker for new inventory requests and generate a corresponding
request in the Finance system.
"""
from pprint import pprint as print
import pdb

import knackpy
import requests

import logging
from _models import Record
from secrets import *


def post_record(record, auth, obj_key, method):

    res = knackpy.record(
        record,
        obj_key=obj_key,
        app_id=auth["app_id"],
        api_key=auth["api_key"],
        method=method,
    )

    return res


def main(src_app_id, dest_app_id, record, record_type):

    src_app_auth = KNACK_CREDENTIALS[src_app_id]
    dest_app_auth = KNACK_CREDENTIALS[dest_app_id]
    src_app_name = KNACK_CREDENTIALS[src_app_id]["name"]
    dest_app_name = KNACK_CREDENTIALS[dest_app_id]["name"]

    record = Record(src_app_name, dest_app_name, record, record_type=record_type)

    dest_obj = record.objects.get(dest_app_name).get("id")

    try:
        res = post_record(
            record.payload, KNACK_CREDENTIALS[dest_app_id], dest_obj, record.method
        )

    except Exception as e:
        return 400, str(e)

    # we flip src/dest here to update the src app with record values from the created/updated record
    record = Record(dest_app_name, src_app_name, res, record_type=record_type)

    dest_obj = record.objects.get(src_app_name).get("id")

    try:
        res = post_record(
            record.payload, KNACK_CREDENTIALS[src_app_id], dest_obj, "update"
        )

    except requests.exceptions.RequestException as e:
        # todo: test
        return e.response.status_code, e.response.text

    return 200, "success"


if __name__ == "__main__":
    import logging
    from _logging import get_logger

    logger = get_logger("_inventory_txn")
    logger.setLevel(logging.DEBUG)