"""
Generate a link on the markings work orders object to the flex notes
page of the connected service request.
"""
import knackpy

# import _setpath
# from scripts import set_env_vars
from atd_knack_api._knack_config import MARKINGS_WORK_ORDERS_FLEX_NOTES as cfg
from atd_knack_api.secrets import KNACK_CREDENTIALS
from atd_knack_api._utils import knackpy_wrapper, knack_filter


def flex_notes_url(record_id):
    return f"https://atd.knack.com/signs-markings#service-requests-markings/view-csr-markings-details/{record_id}/view-markings-flex-notes/{record_id}/"


def main(app_id):

    auth = KNACK_CREDENTIALS[app_id]

    work_orders = knackpy_wrapper(cfg["work_orders"], auth, raw_connections=True)

    if not work_orders.data:
        return 200, "no data to process"

    for wo in work_orders.data_raw:
        payload = {}

        sr_id = wo.get(cfg["work_orders"]["sr_record_id_field"])[0].get("id")

        payload["id"] = wo.get("id")

        payload[cfg["work_orders"]["flex_notes_url_field_id"]] = flex_notes_url(sr_id)

        print(sr_id)

        res = knackpy.record(
            payload,
            obj_key=cfg["work_orders"]["ref_obj"][0],
            app_id=auth["app_id"],
            api_key=auth["api_key"],
            method="update",
            timeout=50,
        )

    return 200, f"{len(payload)} records processed."


if __name__ == "__main__":
    main("5d13ae5b438091000ac0197d")
