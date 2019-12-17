"""
Check Data Tracker for new inventory requests and generate a corresponding
request in the Finance system.
"""
from pprint import pprint as print
import pdb

import knackpy

from _logging import get_logger
from _models import RecordMap
from secrets import *

# todo
# condtionally show "request all" button? and move to right of add items form?
# if we're going to have 1 request per work order, we need to track "issued to" at the transaction level
# and we need to look at/refactor the approval process and post-issue workflow
# integrate task orders??? (yes :( )
# reorg / fix imports
# cance/edit functionality for "requested" transactions
# what is the difference between transaction types "REQUEST" and "WORK ORDER"
# what is the purpose of the UNSUBMITTED field?
# what is the purpose of the Approval Needed field?
# implment inventory request approval in data tracker and set request status based on it. but have to make sure only unsent transactions are approved/modified
# set request approval automatically
# get finance inventory item ids in data tracker
# create function to automatically add user to finance system, or at least get their finance account id into the data tracker- see user_accounts.py

DATA_TRACKER_CONFIG = {
    "transactions": {
        "view": "view_2663",
        "scene": "scene_514",
        "ref_obj": None,
        "obj": None,
    }
}

# move elsewhere
inv_request_obj = "object_25"
inv_txn_finance_obj = "object_23"
inv_txn_data_tracker_obj = "object_36"
work_order_request_id_field = "field_3444"
work_orders_obj = "object_31"
finance_inventory_request_id_on_transaction = "field_3445"
finance_txn_record_id_field = "field_3443"
data_tracker_txn_transmission_status = "field_3448"
work_order_finance_account_id = "field_3449"
work_order_transaction_status_field = "field_1416"

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


def create_inventory_request(work_order, src_app_id, dest_app_id):
    """
    Create new inventory request and update the work order in Data Tracker 
    with the request ID
    """
    request = RecordMap(work_order, type_="inventory_request")

    # todo: implement user-create method

    res = post_record(
        request.payload, KNACK_CREDENTIALS[dest_app_id], inv_request_obj, "create"
    )

    # update data tracker work order with inventory request id
    req_id = res.get("id")

    payload = {"id": work_order.get("id"), work_order_request_id_field: req_id}

    res = post_record(payload, KNACK_CREDENTIALS[src_app_id], work_orders_obj, "update")

    return req_id


def filter_unsent_transactions_on_work_order(request_id):
    """
    Filter to query transactions connected to the inpurt `request_id`.
    Note that the view is pre-filtered in Data Tracker to include only
    those with `transaction_status` == `READY_TO_SEND`
    """
    return [
        {
            "field": finance_inventory_request_id_on_transaction,
            "operator": "is",
            "value": request_id,
        }
    ]


def create_txn(txn_data_tracker, src_app_id, dest_app_id):
    """
    Create or update a transaction record in the finance system from the Data Tracker.
    """
    txn = RecordMap(txn_data_tracker, type_="inventory_transaction")

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
        "id": txn_data_tracker.get("id"),
        finance_txn_record_id_field: txn_id,
        data_tracker_txn_transmission_status: "SENT",
    }

    res = post_record(
        payload, KNACK_CREDENTIALS[src_app_id], inv_txn_data_tracker_obj, "update"
    )

    return res


def main(src_app_id, dest_app_id, work_order):

    auth_data_tracker = KNACK_CREDENTIALS[src_app_id]

    auth_finance_admin = KNACK_CREDENTIALS[dest_app_id]

    request_id = work_order.get(work_order_request_id_field)

    if not request_id:
        logger.debug("Creating new inventory request")
        request_id = create_inventory_request(work_order, src_app_id, dest_app_id)

    filters = filter_unsent_transactions_on_work_order(request_id)

    # get inventory requests from Data Tracker
    logger.debug("Getting unsent transactions.")

    txns = knackpy_wrapper(
        DATA_TRACKER_CONFIG["transactions"], auth_data_tracker, filters=filters
    )

    for txn in txns.data_raw:
        res = create_txn(txn, src_app_id, dest_app_id)


if __name__ == "__main__":
    import logging

    logger = get_logger("_inventory_requests")
    logger.setLevel(logging.DEBUG)

    work_order = {
        "id": "5df10bf86d76b100157d1003",
        "field_1752": "Yes",
        "field_1752_raw": True,
        "field_458": '<span class="581602e43285e4a22c90de05">John Clary</span>',
        "field_458_raw": [
            {"id": "581602e43285e4a22c90de05", "identifier": "John Clary"}
        ],
        "field_1439": "",
        "field_849": "12/11/2019 9:32am",
        "field_849_raw": {
            "date": "12/11/2019",
            "date_formatted": "12/11/2019",
            "hours": "09",
            "minutes": "32",
            "am_pm": "AM",
            "unix_timestamp": 1576056720000,
            "iso_timestamp": "2019-12-11T09:32:00.000Z",
            "timestamp": "12/11/2019 09:32 am",
            "time": 572,
        },
        "field_2701": 2019,
        "field_2701_raw": 2019,
        "field_2700": 2020,
        "field_2700_raw": 2020,
        "field_1421": '<span class="581602e43285e4a22c90de05">John Clary</span>',
        "field_1421_raw": [
            {"id": "581602e43285e4a22c90de05", "identifier": "John Clary"}
        ],
        "field_1074": "12/11/2019 9:32am",
        "field_1074_raw": {
            "date": "12/11/2019",
            "date_formatted": "12/11/2019",
            "hours": "09",
            "minutes": "32",
            "am_pm": "AM",
            "unix_timestamp": 1576056720000,
            "iso_timestamp": "2019-12-11T09:32:00.000Z",
            "timestamp": "12/11/2019 09:32 am",
            "time": 572,
        },
        "field_1600": "12/11/2019 09:32",
        "field_1600_raw": {
            "date": "12/11/2019",
            "date_formatted": "12/11/2019",
            "hours": "09",
            "minutes": "32",
            "am_pm": "AM",
            "unix_timestamp": 1576056720000,
            "iso_timestamp": "2019-12-11T09:32:00.000Z",
            "timestamp": "12/11/2019 09:32 am",
            "time": 572,
        },
        "field_1599": "",
        "field_968": "TMC",
        "field_968_raw": "TMC",
        "field_977": "Other / No Asset",
        "field_977_raw": "Other / No Asset",
        "field_1004": "Trouble Call",
        "field_1004_raw": "Trouble Call",
        "field_976": "Other",
        "field_976_raw": "Other",
        "field_900": "",
        "field_900_raw": [None],
        "field_1420": "TEST WORK ORDER",
        "field_1420_raw": "TEST WORK ORDER",
        "field_2904": "",
        "field_995": "Other",
        "field_995_raw": "Other",
        "field_1006": "No",
        "field_1006_raw": False,
        "field_460": "",
        "field_460_raw": "",
        "field_463": "",
        "field_463_raw": "",
        "field_1351": "",
        "field_1352": "",
        "field_509": "",
        "field_1007": "",
        "field_1007_raw": "",
        "field_888": "2.00",
        "field_888_raw": 2,
        "field_904": "123 FAKE ST",
        "field_904_raw": "",
        "field_1754": '<span class="581602e43285e4a22c90de05">John Clary</span>',
        "field_1754_raw": [
            {"id": "581602e43285e4a22c90de05", "identifier": "John Clary"}
        ],
        "field_909": "",
        "field_909_raw": [],
        "field_913": 2,
        "field_913_raw": 2,
        "field_969": "",
        "field_1353": "No",
        "field_1353_raw": False,
        "field_1354": "No",
        "field_1354_raw": False,
        "field_1003": "TROUBLE CALL",
        "field_1003_raw": "TROUBLE CALL",
        "field_1008": "Wednesday",
        "field_1008_raw": "Wednesday",
        "field_1187": "John Clary",
        "field_1187_raw": "John Clary",
        "field_1215": "No",
        "field_1215_raw": False,
        "field_1374": "No",
        "field_1374_raw": False,
        "field_455": 14160,
        "field_455_raw": 14160,
        "field_1203": 100070800,
        "field_1203_raw": 100070800,
        "field_1204": "WRK",
        "field_1204_raw": "WRK",
        "field_1205": 2019,
        "field_1205_raw": 2019,
        "field_1206": "19",
        "field_1206_raw": "19",
        "field_1207": "070800",
        "field_1207_raw": "070800",
        "field_1208": "WRK19-070800",
        "field_1208_raw": "WRK19-070800",
        "field_1209": "WRK19-070800",
        "field_1209_raw": "WRK19-070800",
        "field_1069": "Other (John Clary)",
        "field_1069_raw": "Other (John Clary)",
        "field_1235": "",
        "field_1235_raw": [],
        "field_1598": "",
        "field_1839": "No",
        "field_1839_raw": False,
        "field_1060": "",
        "field_1859": "",
        "field_1862": "",
        "field_1863": "",
        "field_1864": "",
        "field_1871": "",
        "field_1962": "",
        "field_1971": "",
        "field_2075": "",
        "field_2074": "",
        "field_2059": "No",
        "field_2059_raw": False,
        "field_1972": "Trouble Call",
        "field_1972_raw": "Trouble Call",
        "field_1973": "",
        "field_1974": "",
        "field_1975": "",
        "field_1975_raw": [None],
        "field_2009": "",
        "field_2079": "",
        "field_2079_raw": "",
        "field_2080": "",
        "field_2080_raw": "",
        "field_2081": "",
        "field_2081_raw": "",
        "field_2082": "",
        "field_2082_raw": "",
        "field_2083": "",
        "field_2083_raw": "",
        "field_2084": "",
        "field_2084_raw": "",
        "field_2078": "",
        "field_2085": "",
        "field_2085_raw": "",
        "field_2086": "",
        "field_2086_raw": "",
        "field_2634": "",
        "field_2634_raw": [],
        "field_2695": 0,
        "field_2695_raw": 0,
        "field_2696": 0,
        "field_2696_raw": 0,
        "field_2690": 1,
        "field_2690_raw": 1,
        "field_2691": 0,
        "field_2691_raw": 0,
        "field_2692": 0,
        "field_2692_raw": 0,
        "field_2693": 0,
        "field_2693_raw": 0,
        "field_2694": 0,
        "field_2694_raw": 0,
        "field_2689": "Assigned",
        "field_2689_raw": "Assigned",
        "field_459": "Assigned",
        "field_459_raw": "Assigned",
        "field_3066": 0,
        "field_3066_raw": 0,
        "field_3067": 0,
        "field_3067_raw": 0,
        "field_3068": 0,
        "field_3068_raw": 0,
        "field_3444": "5df63fb5668f810015c601ea",
        "field_3449": "5b422cb82d916c3327423d41",
    }
    main("5815f29f7f7252cc2ca91c4f", "5b422c9b13774837e54ed814", work_order)
