"""
Sanic server for integrating external functions and services.

Add something like this to data tracker:

$(document).on('knack-form-submit.view_2662', function(event, view, record) {
    var payload = JSON.stringify(record)
    $.post("http://localhost:8000/inventory_request?src=5815f29f7f7252cc2ca91c4f&dest=5b422c9b13774837e54ed814", payload).done(function (data) {
        console.log(data);
    });
});

test:
http://localhost:8000/inventory_request?src=5815f29f7f7252cc2ca91c4f&dest=5b422c9b13774837e54ed814&work_order=5df10bf86d76b100157d1003

"""
from datetime import datetime
import logging
import pdb

from sanic import Sanic
from sanic import response
from sanic import exceptions
from sanic_cors import CORS, cross_origin

import _inventory_request

app = Sanic()
CORS(app)


def _403(error):
    raise exceptions.Forbidden(error)


@app.route("/")
async def index(request):
    now = datetime.now().isoformat()
    return response.text(f"ATD Knack API online at {now}")


@app.route("/inventory_request", methods=["POST"])
async def inventory_request(request):
    """
    Listen for an inventory request from a source (`src`) application and
    generate a corresponding request in the destination (`dest`) app.
    """
    src = request.args.get("src")
    dest = request.args.get("dest")
    work_order = request.json

    if not src or not dest:
        _403("`src` and `dest` are required.")

    elif not work_order:
        _403("`work_order` json is required.")

    try:
        res = _inventory_request.main(src, dest, work_order)

    except Exception as e:
        # todo: debug only. this is not safe!
        # return a 5xx error instead.
        raise exceptions.ServerError(f"{e.__class__.__name__}: {e}")

    return response.json(res)


if __name__ == "__main__":
    # todo: remove debug
    # todo: setup proper logging
    logging.basicConfig(filename="error.log", level=logging.DEBUG)
    app.run(debug=True, host="0.0.0.0", port=8000)
