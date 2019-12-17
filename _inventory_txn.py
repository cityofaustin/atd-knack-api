"""
Check Data Tracker for new inventory requests and generate a corresponding
request in the Finance system.
"""
from pprint import pprint as print
import pdb

import knackpy

import logging
from _models import RecordMap
from secrets import *


DATA_TRACKER_CONFIG = {
    "transactions": {
        "view": "view_2663",
        "scene": "scene_514",
        "ref_obj": None,
        "obj": None,
    }
}

FINANCE_TXN_CONFIG = {
    "transactions": {
        "view": "view_694",
        "scene": "scene_84",
        "ref_obj": None,
        "obj": None,
    }
}


# todo: move elsewhere
data_tracker_inv_txn_obj = "object_36"
finance_inv_txn_obj = "object_23"
finance_inv_req_id_transaction_field = "field_790"
finance_inv_req_id_field = "field_570"
finance_submitted_to_data_tracker_field = "field_789"


def post_record(record, auth, obj_key, method):

    res = knackpy.record(
        record,
        obj_key=obj_key,
        app_id=auth["app_id"],
        api_key=auth["api_key"],
        method=method,
    )

    return res


def knackpy_wrapper(cfg_dataset, auth, filters=None):
    return knackpy.Knack(
        obj=cfg_dataset["obj"],
        scene=cfg_dataset["scene"],
        view=cfg_dataset["view"],
        ref_obj=cfg_dataset["ref_obj"],
        app_id=auth["app_id"],
        # api_key=auth["api_key"],
        filters=filters,
        page_limit=1,
        rows_per_page=10,
    )


def filter_unsent_transactions_on_inventory_request(request_id):
    """
    Filter to query transactions connected to the input `request_id`.
    Note that the view is pre-filtered in Finance System to include only
    those with `transaction_status` == `READY_TO_SEND`
    """
    return [
        {
            "field": finance_inv_req_id_transaction_field,
            "operator": "is",
            "value": request_id,
        }
    ]


def issue_item(txn, src_app_id, dest_app_id):
    item = RecordMap(txn, type_="issue_item")
    return post_record(
        item.payload, KNACK_CREDENTIALS[dest_app_id], data_tracker_inv_txn_obj, "update"
    )


def main(src_app_id, dest_app_id, inv_request):

    auth_data_tracker = KNACK_CREDENTIALS[dest_app_id]

    auth_finance_admin = KNACK_CREDENTIALS[src_app_id]

    request_id = inv_request.get(finance_inv_req_id_field)

    filters = filter_unsent_transactions_on_inventory_request(request_id)

    txns = knackpy_wrapper(
        FINANCE_TXN_CONFIG["transactions"], auth_finance_admin, filters=filters
    )

    for txn in txns.data_raw:
        res = issue_item(txn, src_app_id, dest_app_id)

        # update finance system transaction as submitted
        payload = {"id": txn.get("id"), finance_submitted_to_data_tracker_field: True}

        res = post_record(payload, auth_finance_admin, finance_inv_txn_obj, "update")

    return {"records_processed": f"{len(txns.data_raw)}"}

    # get inventory requests from Data Tracker
    logging.debug("Getting unsent transactions.")


if __name__ == "__main__":
    import logging
    from _logging import get_logger

    logger = get_logger("_inventory_txn")
    logger.setLevel(logging.DEBUG)

    inv_request = {
        "id": "5df8374417698d001aaa65bb",
        "field_570": 41,
        "field_570_raw": 41,
        "field_767": "5df10bf86d76b100157d1003",
        "field_767_raw": "5df10bf86d76b100157d1003",
    }

    main("5b422c9b13774837e54ed814", "5815f29f7f7252cc2ca91c4f", inv_request)
