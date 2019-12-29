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

inv_txn_finance_obj = "object_23"
inv_txn_data_tracker_obj = "object_36"
finance_txn_record_id_field = "field_3443"
data_tracker_txn_transmission_status = "field_3448"
data_tracker_txn_submitted_to_finance = "field_3453"

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

    txn_response = post_record(
        txn.payload, KNACK_CREDENTIALS[dest_app_id], inv_txn_finance_obj, method
    )

    txn2 = RecordMap(dest_app_name, src_app_name, txn_response, type_="inventory_txn", direction="to_data_tracker")

    res = post_record(
        txn2.payload, KNACK_CREDENTIALS[src_app_id], inv_txn_data_tracker_obj, "update"
    )

    pdb.set_trace()
    return res


def main(src_app_id, dest_app_id, data):

    src_app_auth = KNACK_CREDENTIALS[src_app_id]
    dest_app_auth = KNACK_CREDENTIALS[dest_app_id]

    src_app_name = KNACK_CREDENTIALS[src_app_id]["name"]
    dest_app_name = KNACK_CREDENTIALS[dest_app_id]["name"]

    """
    TODO not tested
    """
    if "finance" in src_app_name.lower():
        direction = "to_data_tracker"

    elif "data_tracker" in src_app_name.lower():
        direction = "to_finance_system"

    res = handle_txn(txn, src_app_id, dest_app_id, direction=direction)

    return res


if __name__ == "__main__":
    import logging
    from _logging import get_logger
    logger = get_logger("_inventory_txn")
    logger.setLevel(logging.DEBUG)
    txn = {'field_1071': 'New', 'field_1071_raw': 'New', 'field_1196': '12/25/2019 10:29pm', 'field_1196_raw': {'am_pm': 'PM', 'date': '12/25/2019', 'date_formatted': '12/25/2019', 'hours': '10', 'iso_timestamp': '2019-12-25T22:29:00.000Z', 'minutes': '29', 'time': 1349, 'timestamp': '12/25/2019 10:29 pm', 'unix_timestamp': 1577312940000}, 'field_1202': '<span class="581602e43285e4a22c90de05">John Clary</span>', 'field_1202_raw': [{'id': '581602e43285e4a22c90de05', 'identifier': 'John Clary'}], 'field_1409': 0, 'field_1409_raw': 0, 'field_1410': '', 'field_1412': 'Assigned', 'field_1412_raw': 'Assigned', 'field_1416': 'Submitted to Warehouse', 'field_1416_raw': 'Submitted to Warehouse', 'field_2476': 'No', 'field_2476_raw': False, 'field_2478': '$84.0000', 'field_2478_raw': 84, 'field_2479': '$840.0000', 'field_2479_raw': 840, 'field_2481': 'No', 'field_2481_raw': False, 'field_2486': '', 'field_2716': '<span class="581602e43285e4a22c90de05">John Clary</span>', 'field_2716_raw': [{'id': '581602e43285e4a22c90de05', 'identifier': 'John Clary'}], 'field_3387': '199', 'field_3387_raw': '199', 'field_3439': '$84.00', 'field_3439_raw': '$84.00', 'field_3440': 'Yes', 'field_3440_raw': True, 'field_3441': 'Yes', 'field_3441_raw': True, 'field_3443': '5e043f63a7d5e60015c08183', 'field_3443_raw': '5e043f63a7d5e60015c08183', 'field_3445': '5e043f54933e8200153902cf', 'field_3445_raw': '5e043f54933e8200153902cf', 'field_3447': '5e0820f03245070015fb14b3', 'field_3447_raw': '5e0820f03245070015fb14b3', 'field_3448': 'SENT', 'field_3448_raw': 'SENT', 'field_3451': '5b773da5fb0fe322c390274b', 'field_3451_raw': '5b773da5fb0fe322c390274b', 'field_3452': '<span class="581602e43285e4a22c90de05">John Clary</span>', 'field_3452_raw': [{'id': '581602e43285e4a22c90de05', 'identifier': 'John Clary'}], 'field_3453': 'Yes', 'field_3453_raw': True, 'field_513': '<span class="5dfa6ac42057600ac95e792e">100 Amp Breaker Panel | EA</span>', 'field_513_raw': [{'id': '5dfa6ac42057600ac95e792e', 'identifier': '100 Amp Breaker Panel | EA'}], 'field_514': '<span class="5df10bf86d76b100157d1003">WRK19-070800</span>', 'field_514_raw': [{'id': '5df10bf86d76b100157d1003', 'identifier': 'WRK19-070800'}], 'field_524': '10.00', 'field_524_raw': 10, 'field_768': '', 'field_769': 'WORK ORDER', 'field_769_raw': 'WORK ORDER', 'field_770': 6501, 'field_770_raw': 6501, 'field_771': '12/25/2019 22:29', 'field_771_raw': {'am_pm': 'PM', 'date': '12/25/2019', 'date_formatted': '12/25/2019', 'hours': '10', 'iso_timestamp': '2019-12-25T22:29:00.000Z', 'minutes': '29', 'time': 1349, 'timestamp': '12/25/2019 10:29 pm', 'unix_timestamp': 1577312940000}, 'field_854': '', 'id': '5e04372f11440400184d79f0'}
    main("5815f29f7f7252cc2ca91c4f", "5b422c9b13774837e54ed814", txn)
