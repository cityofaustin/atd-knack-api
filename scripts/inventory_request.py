"""
Check Data Tracker for new inventory requests and generate a corresponding
request in the Finance system.
"""
from pprint import pprint as print
import pdb

import knackpy


# store field config locally to limit # of requests
# query transactions
# check if work order/request exists
# parse data to create request if needed
# check existing inventory transacitons
# add inventory transactions

KNACK_CREDENTIALS = {
    "5815f29f7f7252cc2ca91c4f" : {
        "name" : "Data Tracker Prod",
        "app_id" : "5815f29f7f7252cc2ca91c4f"
    }
}

DATA_TRACKER_CONFIG = {
    "transactions" : {
        "view" : "view_2663",
        "scene" : "scene_514",
        "ref_obj" : None,
        "obj" : None
    }
}



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


def map_fields(list_of_dicts, fieldmap):
    mapped = []

    for record in list_of_dicts:
        new_record = {}

        for key in record.keys():
            if key in FIELDMAP.keys():
                new_record[FIELDMAP[key]] = record[key]

        mapped.append(new_record)

    return mapped


def main(src_app_id, dest_app_id):

    auth_data_tracker = KNACK_CREDENTIALS[src_app_id]

    # auth_finance_admin = KNACK_CREDENTIALS[dest_app_id]

    # get inventory requests from Data Tracker
    inv_reqs = knackpy_wrapper(
        DATA_TRACKER_CONFIG["transactions"], auth_data_tracker
    )

    if not inv_reqs.data_raw:
        return 0

    else:
        return inv_reqs.data_raw


if __name__ == "__main__":
    main("abc", "123")