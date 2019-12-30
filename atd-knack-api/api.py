"""
Sanic server for integrating external functions and services to Knack.
"""
from datetime import datetime
import logging
import pdb

from sanic import Sanic
from sanic import response
from sanic import exceptions
from sanic_cors import CORS, cross_origin

from _fieldmaps import FIELDMAP
from _logging import get_logger
import _record
from secrets import KNACK_CREDENTIALS

app = Sanic()
CORS(app)


def _403(error):
    raise exceptions.Forbidden(error)


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
async def index(request):
    now = datetime.now().isoformat()
    return response.text(f"ATD Knack API online at {now}")


@app.route("/record", methods=["POST"])
async def record(request):
    """
    Facilitates record transformation and copying between Knack applications.
    Currently supports the exchange of inventory-related records between
    Data Tracker and the Finance and Purchasing System.
    
    This service is designed for two-way communication between Knack applications,
    and requires appropriate conifguration in the source and destination
    applications. Notably, records in each application will need dedicated fields
    to store the Knack record UUID of the cooresponding record in it's complement
    application. This allows existing records to be updated, rather than created,
    and it enables the setting of record connections across Knack objects. 

    Request Parameters
    ----------
    src : str (required)
        The application ID of the source application
    
    dest : str (required)
        The application ID of the destination application

    record_type : str (required)
        The type of record to be transmitted. This value is used to retrieve the
        correct fieldmap definitions which will be applied to the record translation.
        Valide `record_type`s are defined in _fieldmaps.py.

    data : Content-Type:application/json (required)
        The Knack record data to be transmitted.
    
    Requests are handled like so:
    
    1. An API request is initated by custom CORS request that has been configured in
    the source Knack application, typically after a form submission event.

    2. The API validates that all required values are present, and validates that the
    `src` and `dest` application IDs are known defined `secrets.py`, and that the
    requested `record_type` is defined in `fieldmaps.py`.

    3. Request data is translated to a new request payload according to its fieldmap.
    
    4. The translated source data is posted to the destination application.

    5. The responsde data from the destination application is then translated to
    the format of source application, and source application is updated accordingly.
    
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
    data = request.json
    record_type = request.args.get("type")
    print(request)
    if not src or not dest:
        _403("`src` and `dest` are required.")

    if not data:
        _403("`data` json is required.")

    if not record_type:
        _403("Record `type` is required.")

    if not _valid_app_ids([src, dest]):
        _403("Unknown `src` or `dest` application ID(s) provided.")

    if not _valid_record_type(record_type):
        _403("Unknown record `type` provided.")

    try:
        status_code, message = _record.main(src, dest, data, record_type=record_type)

    except Exception as e:
        # todo: debug only. this is not safe!
        # return a 5xx error instead.
        raise exceptions.ServerError(f"{e.__class__.__name__}: {e}")

    if status_code == 200:
        return response.text(message)

    else:
        raise ServerError(message, status_code=500)


if __name__ == "__main__":
    # todo: remove debug logging
    logger = get_logger("api")
    logger.setLevel(logging.DEBUG)
    app.run(debug=True, host="0.0.0.0", port=8000)
