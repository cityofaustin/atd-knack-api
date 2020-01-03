"""
Flask server for integrating external functions and services to Knack.
"""
from datetime import datetime
import logging
import pdb

from flask import Flask, request, abort
from flask_cors import CORS

from _fieldmaps import FIELDMAP
from _logging import get_logger
import _inventory
from secrets import KNACK_CREDENTIALS

app = Flask(__name__)
CORS(app)


def _403(error):
    abort(error)


def _valid_app_ids(app_ids):
    """
    Ensure that the requested application IDs exist in the credential store.
    """
    for app_id in app_ids:
        try:
            app_data = KNACK_CREDENTIALS[app_id]

        except KeyError:
            return False

    return True


def _valid_record_type(record_type):
    try:
        fieldmap = FIELDMAP[record_type]

    except KeyError:
        return False

    return True


@app.route("/")
def index():
    now = datetime.now().isoformat()
    return f"ATD Knack API online at {now}"


@app.route("/inventory", methods=["POST"])
def record():
    """
    Facilitates transformation and copying of inventory records between the Finance
    System and the Data Tracker.

    This service is designed for two-way communication between Knack applications,
    and requires appropriate conifguration in the source and destination
    applications. Notably, records in each application will need dedicated fields
    to store the Knack record UUID of the corresponding record in it's complement
    application. This allows existing records to be updated, rather than created,
    and it enables the setting of record connections across Knack objects. 

    Request Parameters
    ----------
    src : str (required)
        The application ID of the source application
    
    dest : str (required)
        The application ID of the destination application

     Requests are handled like so:
    
    1. An API request is initated by a custom CORS request that has been configured in
    the source Knack application, typically after a form submission event.

    2. The API validates that all required values are present, and validates that the
    `src` and `dest` application IDs are defined `secrets.py`.

    3. The request triggers `_inventory.py`, which fetches work order records
    (if the source is Data Tracker) or inventory requests (if the source is the
    Finance Sytem), as well as related inventory trasnactions from pre-configured
    Knack API views whose records are "READY_TO_SEND". Records are translated
    from the source application to the destination application according to
    `_fieldmaps.py`.
    
    4. Translated records are posted to the destination application. The Knack
    API responds with a record from the destination application, which is translated
    back to the format of the source application using the "callback" fieldmap,
    and the source application is in turn updated.
    
    So, this endpoint triggers two record updates in response to
    any request:
        1) a record is created or updated in the destination application.
        2) the originating record is updated in the src application.
    
    This behavior exists so that any time a record is created in a destination app
    the original record is updated with additional data about it's state. E.g.,
    updating a field which confirms that transmission was successful, or updating
    the source record with Knack record ID in the destination application, which 
    ensures that future record updates are processed as an update rather than a new record.

    See `_fieldmaps.py` for further documentation on the mechanics of record translation,
    notably the use of the `direction` parameter.
    """
    src = request.args.get("src")
    dest = request.args.get("dest")
    
    if not src or not dest:
        _403("`src` and `dest` are required.")

    if not _valid_app_ids([src, dest]):
        _403("Unknown `src` or `dest` application ID(s) provided.")

    try:
        status_code, message = _inventory.main(src, dest)

    except Exception as e:
        # todo: debug only. this is not safe!
        # return a 5xx error instead.
        raise exceptions.ServerError(f"{e.__class__.__name__}: {e}")

    if status_code == 200:
        return message

    else:
        abort(503, message)


if __name__ == "__main__":
    # todo: remove debug logging
    logger = get_logger("api")
    logger.setLevel(logging.DEBUG)
    app.run(debug=True, host="0.0.0.0", port=8000)
