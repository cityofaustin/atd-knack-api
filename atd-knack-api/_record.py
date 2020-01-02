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


def main(app_id_src, app_id_dest, record, record_type):

    app_auth_src = KNACK_CREDENTIALS[app_id_src]
    app_auth_dest = KNACK_CREDENTIALS[app_id_dest]
    app_name_src = KNACK_CREDENTIALS[app_id_src]["name"]
    app_name_dest = KNACK_CREDENTIALS[app_id_dest]["name"]

    record = Record(app_name_src, app_name_dest, record, record_type=record_type)

    dest_obj = record.knack_cfg.get(app_name_dest).get("object")

    try:
        res = post_record(
            record.payload, KNACK_CREDENTIALS[app_id_dest], dest_obj, record.method
        )

    except Exception as e:
        return 400, str(e)

    # we flip src/dest here to update the src app with record values from the created/updated record
    record = Record(app_name_dest, app_name_src, res, record_type=record_type)

    dest_obj = record.knack_cfg.get(app_name_src).get("object")

    try:
        res = post_record(
            record.payload, KNACK_CREDENTIALS[app_id_src], dest_obj, "update"
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