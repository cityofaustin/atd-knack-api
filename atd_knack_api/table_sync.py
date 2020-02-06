"""
Synchronize two knack objects across Knack applications.
"""


# import knackpy

# use the record model
# detect new
# compare changes?
# archive status?
# keep it simple - task orders and accounts
# field: field
# transform
# direction

import logging
from pprint import pprint as print

import requests

import _setpath # uncomment this for local development
from scripts import set_env_vars
from atd_knack_api._fieldmaps import FIELDMAP
from atd_knack_api._models import Record
from atd_knack_api.secrets import KNACK_CREDENTIALS
from atd_knack_api._utils import knackpy_wrapper


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

    record_type = "accounts"

    cfg = FIELDMAP[record_type]["knack_cfg"][app_name_src]

    accounts_src = knackpy_wrapper(cfg, KNACK_CREDENTIALS[app_id_src])

    accounts_dest = knackpy_wrapper(cfg, KNACK_CREDENTIALS[app_id_dest])
    
    ### use fieldmap to compare new vs existing
    ### HMM
    for inv_req in inv_reqs.data_raw:
        res = handle_request(app_id_src, app_id_dest, inv_req, record_type)


    return 200, "success"


if __name__ == "__main__":
    import logging
    from _logging import get_logger

    logger = get_logger("_inventory_txn")
    logger.setLevel(logging.DEBUG)
    # 5e2216f0cbf8d9001616b034 data tracker test
    main("5e2216f0cbf8d9001616b034", "5b422c9b13774837e54ed814")
