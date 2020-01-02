"""
Check Data Tracker for new inventory requests and generate a corresponding
request in the Finance system.
"""
import logging
from pprint import pprint as print
import pdb

import knackpy
import requests

from _fieldmaps import FIELDMAP
from _models import Record
from secrets import *


def knackpy_wrapper(cfg, app_id):
    """
    Fetch records which need to be processed from a pre-filtered
    Knack view which does not require authentication.
    """
    return knackpy.Knack(
        scene=cfg["scene"],
        view=cfg["view"],
        app_id=app_id,
        page_limit=1,
        rows_per_page=10,
    )


def post_record(record, auth, obj_key, method):

    res = knackpy.record(
        record,
        obj_key=obj_key,
        app_id=auth["app_id"],
        api_key=auth["api_key"],
        method=method,
    )

    return res


def handle_request(app_id_src, app_id_dest, data, record_type):

    record = Record(app_id_src, app_id_dest, data, record_type=record_type)

    res = record.send()

    """
    We flip src/dest here to "callback" to the src app with record values from the 
    created/updated record.
    """
    record = Record(
        app_id_dest, app_id_src, res, record_type=record_type, callback=True
    )

    res = record.send()

    return res


def main(app_id_src, app_id_dest):
    app_name_src = KNACK_CREDENTIALS[app_id_src]["name"]

    record_type = "inventory_request"

    cfg = FIELDMAP[record_type]["knack_cfg"][app_name_src]

    inv_reqs = knackpy_wrapper(cfg, app_id_src)

    for inv_req in inv_reqs.data_raw:
        res = handle_request(app_id_src, app_id_dest, inv_req, record_type)

    record_type = "inventory_txn"

    cfg = FIELDMAP[record_type]["knack_cfg"][app_name_src]

    inv_txns = knackpy_wrapper(cfg, app_id_src)

    for inv_txn in inv_txns.data_raw:
        res = handle_request(app_id_src, app_id_dest, inv_txn, record_type)

    return 200, "success"


if __name__ == "__main__":
    import logging
    from _logging import get_logger

    logger = get_logger("_inventory_txn")
    logger.setLevel(logging.DEBUG)

    main("5815f29f7f7252cc2ca91c4f", "5b422c9b13774837e54ed814")
