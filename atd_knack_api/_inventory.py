"""
Handle inventory requests and transactions between the Data Tracker and
the Finance System.
"""
import logging
from pprint import pprint as print

import knackpy
import requests

# import _setpath # uncomment this for local development
from atd_knack_api._fieldmaps import FIELDMAP
from atd_knack_api._models import Record
from atd_knack_api.secrets import KNACK_CREDENTIALS


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

    if cfg.get("scene"):
        """
        We do not define a scene/view for inventory requests coming from the Finance
        System. This is because the work orders are never updated from the Finance
        System. So this ugly bit of logic skips this step for Finance > Data Tracker.
        """
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

    main("src_app_id_here", "dest_app_id_here")
