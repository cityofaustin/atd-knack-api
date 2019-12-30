"""
Sanic server for integrating external functions and services.

Add something like this to data tracker:

$(document).on('knack-form-submit.view_2664', function(event, view, record) {
    var src = Knack.application_id;
    var dest = "5b422c9b13774837e54ed814"; // finance prod
    var payload = JSON.stringify(record);
    var type = "inventory_request";
    $.post("http://localhost:8000/record?src=" + src + "&dest=" + dest + "&type=" + type, payload).done(function (data) {
        console.log(data);

        var token = Knack.getUserToken();
        var headers = {"Authorization": token, 'X-Knack-Application-ID': src};
        var url = "https://api.knack.com/v1/pages/scene_255/views/view_1966/records"
        
        $.ajaxSetup({headers:headers});

        $.get(url, headers=headers).done(function(data) {
            console.log(data)
        })
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
    Handle a Knack record.
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
