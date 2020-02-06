"""
Connect markings work orders to the flex notes that are connected to their connected
311 Service Request.
"""
from pprint import pprint as print
import pdb

import knackpy

# import _setpath
# from scripts import set_env_vars
from atd_knack_api._knack_config import MARKINGS_WORK_ORDERS_FLEX_NOTES as cfg
from atd_knack_api.secrets import KNACK_CREDENTIALS
from atd_knack_api._utils import knackpy_wrapper, knack_filter


def main(app_id):

    auth = KNACK_CREDENTIALS[app_id]

    # gets work orders have a connected CSR, but no flex notes
    # this filtering is done in the knack view
    work_orders = knackpy_wrapper(cfg["work_orders"], auth)

    if not work_orders.data:
        return 200, "no data to process"

    for wo in work_orders.data:
        payload = []

        sr_number = wo.get(cfg["work_orders"]["sr_number_field_name"])

        wo_id = wo.get("id")

        # fetch all flex notes connected to each service request
        # the Knack view is filtered to exclude the "XFERIOSK" flex note
        # which is just "allow record to be published to external interfaces"
        _filter = knack_filter(cfg["flex_notes"]["sr_number_field_id"], sr_number)

        flex_notes = knackpy_wrapper(cfg["flex_notes"], auth, filters=_filter)

        for fn in flex_notes.data_raw:
            fn[cfg["flex_notes"]["work_order_connection_field_id"]] = [wo_id]

            # reduce flex note to record id, work order connection field
            fn_payload = {}

            for key in fn.keys():
                if key in cfg["flex_notes"]["payload_field_ids"]:
                    fn_payload[key] = fn[key]

            payload.append(fn_payload)

        for record in payload:

            res = knackpy.record(
                record,
                obj_key=cfg["flex_notes"]["ref_obj"][0],
                app_id=auth["app_id"],
                api_key=auth["api_key"],
                method="update",
                timeout=50,
            )

    return 200, f"{len(payload)} records processed."


if __name__ == "__main__":
    main("app_id_goes_here")
