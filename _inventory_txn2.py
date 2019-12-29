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

def post_record(record, auth, obj_key, method):

    res = knackpy.record(
        record,
        obj_key=obj_key,
        app_id=auth["app_id"],
        api_key=auth["api_key"],
        method=method,
    )

    return res


def handle_txn(txn, src_app_id, dest_app_id, direction=None):
    """
    Create or update a transaction record.
    """
    src_app_name = KNACK_CREDENTIALS[src_app_id]["name"]
    dest_app_name = KNACK_CREDENTIALS[dest_app_id]["name"]

    txn = RecordMap(src_app_name, dest_app_name, txn, type_="inventory_txn", direction=direction)

    if not txn.payload.get("id"):
        method = "create"
    else:
        method = "update"

    res = post_record(
        txn.payload, KNACK_CREDENTIALS[dest_app_id], inv_txn_finance_obj, method
    )

    # update data tracker transaction with transaction ID in finance
    txn_id = res.get("id")

    payload = {
        "id": txn.get("id"),
        finance_txn_record_id_field: txn_id,
        data_tracker_txn_transmission_status: "SENT",
        data_tracker_txn_submitted_to_finance: True,
    }

    res = post_record(
        payload, KNACK_CREDENTIALS[src_app_id], inv_txn_obj, "update"
    )

    return res


def main(src_app_id, dest_app_id, data):

    src_app_auth = KNACK_CREDENTIALS[src_app_id]
    dest_app_auth = KNACK_CREDENTIALS[dest_app_id]

    src_app_name = KNACK_CREDENTIALS[src_app_id]["name"]
    dest_app_name = KNACK_CREDENTIALS[dest_app_id]["name"]

    """
    TODO
    - merging to handle inventory request or work order.
    - handle actions. move actions in fieldmaps to app level
    """

    if "finance" in src_app_name.lower():
        # handle inventory request from finance system
        # todo: move/reduce code from _inventory_txn
        direction = "to_data_tracker"

    elif "data_tracker" in src_app_name.lower():
        # handle work order from data tracker
        direction = "to_finance_system"

        request_id = data.get(work_order_request_id_field)

        if not request_id:
            logging.debug("Creating new inventory request")
            request_id = create_inventory_request(data, src_app_id, dest_app_id)

        pdb.set_trace()
        filters = filter_unsent_transactions_on_work_order(request_id)

        # get inventory requests from Data Tracker
        logging.debug("Getting unsent transactions.")

        txns = knackpy_wrapper(
            DATA_TRACKER_CONFIG["transactions"], src_app_auth, filters=filters
        )

        for txn in txns.data_raw:
            res = handle_txn(txn, src_app_id, dest_app_id, direction=direction)

    else:
        """
        This should never happen because we validate src/dest app IDs when the
        request is received. The KNACK_CREDENTIALS may be corrupted.
        """
        raise Exception("Unknown application ID provided")

    # TODO: return a response ;)


if __name__ == "__main__":
    import logging
    from _logging import get_logger
    logger = get_logger("_inventory_txn")
    logger.setLevel(logging.DEBUG)
    main("5815f29f7f7252cc2ca91c4f", "5b422c9b13774837e54ed814", txn)
