"""
Sanic server for integrating external functions and services.

Add something like this to data tracker:

$(document).on('knack-form-submit.view_2662', function(event, view, record) {
    var payload = JSON.stringify(record)
    $.post("http://localhost:8000/inventory_request?src=5815f29f7f7252cc2ca91c4f&dest=5b422c9b13774837e54ed814", payload).done(function (data) {
        console.log(data);
    });
});
"""
from datetime import datetime
import logging
import pdb

from sanic import Sanic
from sanic import response
from sanic import exceptions
from sanic_cors import CORS, cross_origin

from secrets import KNACK_CREDENTIALS
import _inventory_request
import _inventory_txn
import _create_account

from _logging import get_logger

app = Sanic()
CORS(app)


def _403(error):
    raise exceptions.Forbidden(error)


def _validate_app_ids(app_ids):
    """
    Ensure that the requested application IDs exist in the credential store.
    """
    for app_id in app_ids:
        app_data = KNACK_CREDENTIALS[app_id]

    return True


@app.route("/")
async def index(request):
    now = datetime.now().isoformat()
    return response.text(f"ATD Knack API online at {now}")


@app.route("/inventory_request", methods=["POST"])
async def inventory_request(request):
    """
    TODO: udpate with separate docs for requests/txns
    Facilitates inventory requests between the AMD Data Tracker and the Finance and
    Purchasing system.

    Listens for a work order from the Data Tracker and generates a corresponding
    inventory request in the finance system.
    --- 

    When the request payload is a work order record dict from the Data Tracker,
    it is handled like so:
    
    1. A new inventory request is created in the finance system, if one does not already
    exist for this work order.
    
    2. The _inventory_requests script fetches any `READY_TO_SEND` item "transactions"
    connected to this request.

    3. The work order in the Data Tracker is updated with the Knack record ID of the
    inventory request in the Finance system.
    
    ---

    Record flows from the Finance system to the Data Tracker only occur when transactions
    are updated in the Finance system, i.e., a transaction is issued or cancelled. All
    inventory requests sent to the API from the Finance system will already have a 
    corresponding work order in the Data Tracker, as well as connected transactions. The
    work order in the Data Tracker is never updated by the Finance System, only
    connected transactions are processed.

    When the request payload is an inventory request from the Finance system:
    
    1. The API receives an inventory request, extracts the request ID, and fetches any
    `READY_TO_SEND` item "transactions" connected to the request. These transactions are
    fetched from a pre-filtered table view in the Finacne System.

    2. Corresponding inventory transactions in the Data Tracker are updated accordingly.

    3. The `transmission_status` of theaffected inventory transactions in the Finance sytem
    are updated to confirm the request has been successfully sent to the data tracker.

    """
    src = request.args.get("src")
    dest = request.args.get("dest")

    data = request.json

    if not src or not dest:
        _403("`src` and `dest` are required.")

    elif not data:
        _403("`data` json is required.")

    try:
        # todo: test
        _validate_app_ids([src, dest])

    except:
        _403("Unknown `src` or `dest` application ID(s) provided.")

    try:
        res = _inventory_request.main(src, dest, data)

    except Exception as e:
        # todo: debug only. this is not safe!
        # return a 5xx error instead.
        raise exceptions.ServerError(f"{e.__class__.__name__}: {e}")

    return response.json(res)

@app.route("/inventory_txn", methods=["POST"])
async def inventory_txn(request):
    """
    Handle a transaction.
    """
    src = request.args.get("src")
    dest = request.args.get("dest")
    data = request.json

    if not src or not dest:
        _403("`src` and `dest` are required.")

    elif not data:
        _403("`data` json is required.")

    try:
        # todo: test
        _validate_app_ids([src, dest])

    except:
        _403("Unknown `src` or `dest` application ID(s) provided.")

    try:
        res = _inventory_txn2.main(src, dest, data) #todo: create this

    except Exception as e:
        # todo: debug only. this is not safe!
        # return a 5xx error instead.
        raise exceptions.ServerError(f"{e.__class__.__name__}: {e}")

    return response.json({"todo": "todo"})


@app.route("/create_account", methods=["POST"])
async def create_account(request):
    """
    Create an account in the destination app which mirrors an account
    in the source app.
    """
    src = request.args.get("src")
    dest = request.args.get("dest")
    data = request.json

    if not src or not dest:
        _403("`src` and `dest` are required.")

    elif not data:
        _403("`data` json is required.")

    try:
        res = _create_account.main(src, dest, data)

    except Exception as e:
        # todo: debug only. this is not safe!
        # return a 5xx error instead.
        raise exceptions.ServerError(f"{e.__class__.__name__}: {e}")

    return response.json(res)


if __name__ == "__main__":
    # todo: remove debug logging
    logger = get_logger("api")
    logger.setLevel(logging.DEBUG)
    app.run(debug=True, host="0.0.0.0", port=8000)
