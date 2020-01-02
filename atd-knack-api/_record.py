"""
Check Data Tracker for new inventory requests and generate a corresponding
request in the Finance system.
"""
from pprint import pprint as print
import pdb

import knackpy
import requests

import logging
from _models import Record
from secrets import *


def main(app_id_src, app_id_dest, record, record_type):

    record = Record(app_id_src, app_id_dest, record, record_type=record_type)

    res = record.send()

    """
    We flip src/dest here to "callback" to the src app with record values from the 
    created/updated record.
    """
    record = Record(
        app_id_dest, app_id_src, res, record_type=record_type, callback=True
    )

    res = record.send()

    return 200, "success"


if __name__ == "__main__":
    import logging
    from _logging import get_logger

    logger = get_logger("_inventory_txn")
    logger.setLevel(logging.DEBUG)
