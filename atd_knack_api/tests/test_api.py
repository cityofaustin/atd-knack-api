import pdb

import pytest
import requests

import api
from tests import _config


@pytest.yield_fixture
def app():
    app = api.app
    yield app


@pytest.fixture
def test_cli(loop, app, sanic_client):
    return loop.run_until_complete(sanic_client(app))


@pytest.fixture
def global_config():
    return {
        "data_tracker": _config.DATA_TRACKER,
        "finance_system": _config.FINANCE_SYSTEM,
        "records": _config.RECORDS,
    }


async def test_index(test_cli):
    resp = await test_cli.get("/")
    assert resp.status == 200


async def test_record_invalid_app_id(test_cli, global_config):
    record_type = "inventory_request"
    src_app_id = "abc123"
    dest_app_id = global_config["data_tracker"]

    res = await test_cli.post(
        f"/record?src={src_app_id}&dest={dest_app_id}&type={record_type}",
        json=global_config["records"][record_type],
    )

    assert res.status == 403


async def test_record_missing_body(test_cli, global_config):
    record_type = "inventory_request"
    src_app_id = "abc123"
    dest_app_id = global_config["data_tracker"]

    res = await test_cli.post(
        f"/record?src={src_app_id}&dest={dest_app_id}&type={record_type}",
    )

    assert res.status == 403