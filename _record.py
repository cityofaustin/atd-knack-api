"""
Check Data Tracker for new inventory requests and generate a corresponding
request in the Finance system.
"""
from pprint import pprint as print
import pdb

import knackpy
import requests

import logging
from _models import RecordMap
from secrets import *


def post_record(record, auth, obj_key, method):

    res = knackpy.record(
        record,
        obj_key=obj_key,
        app_id=auth["app_id"],
        api_key=auth["api_key"],
        method=method,
    )

    return res


def main(src_app_id, dest_app_id, record, record_type):

    src_app_auth = KNACK_CREDENTIALS[src_app_id]
    dest_app_auth = KNACK_CREDENTIALS[dest_app_id]
    src_app_name = KNACK_CREDENTIALS[src_app_id]["name"]
    dest_app_name = KNACK_CREDENTIALS[dest_app_id]["name"]

    record = RecordMap(src_app_name, dest_app_name, record, record_type=record_type)

    dest_obj = record.objects.get(dest_app_name).get("id")

    try:
        res = post_record(
            record.payload, KNACK_CREDENTIALS[dest_app_id], dest_obj, record.method
        )

    except Exception as e:
        return 400, str(e)

    # we flip src/dest here to update the src app with record values from the created/updated record
    record = RecordMap(dest_app_name, src_app_name, res, record_type=record_type)

    dest_obj = record.objects.get(src_app_name).get("id")

    try:
        res = post_record(
            record.payload, KNACK_CREDENTIALS[src_app_id], dest_obj, "update"
        )

    except requests.exceptions.RequestException as e:
        # todo: test
        return e.response.status_code, e.response.text

    return 200, "success"


if __name__ == "__main__":
    import logging
    from _logging import get_logger

    logger = get_logger("_inventory_txn")
    logger.setLevel(logging.DEBUG)

    # new transaction
    record = {
        "field_1071": "New",
        "field_1071_raw": "New",
        "field_1196": "12/25/2019 10:29pm",
        "field_1196_raw": {
            "am_pm": "PM",
            "date": "12/25/2019",
            "date_formatted": "12/25/2019",
            "hours": "10",
            "iso_timestamp": "2019-12-25T22:29:00.000Z",
            "minutes": "29",
            "time": 1349,
            "timestamp": "12/25/2019 10:29 pm",
            "unix_timestamp": 1577312940000,
        },
        "field_1202": '<span class="581602e43285e4a22c90de05">John Clary</span>',
        "field_1202_raw": [
            {"id": "581602e43285e4a22c90de05", "identifier": "John Clary"}
        ],
        "field_1409": 0,
        "field_1409_raw": 0,
        "field_1410": "",
        "field_1412": "Assigned",
        "field_1412_raw": "Assigned",
        "field_1416": "Submitted to Warehouse",
        "field_1416_raw": "Submitted to Warehouse",
        "field_2476": "No",
        "field_2476_raw": False,
        "field_2478": "$84.0000",
        "field_2478_raw": 84,
        "field_2479": "$840.0000",
        "field_2479_raw": 840,
        "field_2481": "No",
        "field_2481_raw": False,
        "field_2486": "",
        "field_2716": '<span class="581602e43285e4a22c90de05">John Clary</span>',
        "field_2716_raw": [
            {"id": "581602e43285e4a22c90de05", "identifier": "John Clary"}
        ],
        "field_3387": "199",
        "field_3387_raw": "199",
        "field_3439": "$84.00",
        "field_3439_raw": "$84.00",
        "field_3440": "Yes",
        "field_3440_raw": True,
        "field_3441": "Yes",
        "field_3441_raw": True,
        "field_3443": "5e043f63a7d5e60015c08183",
        "field_3443_raw": "5e043f63a7d5e60015c08183",
        "field_3445": "5e043f54933e8200153902cf",
        "field_3445_raw": "5e043f54933e8200153902cf",
        "field_3447": "5e0820f03245070015fb14b3",
        "field_3447_raw": "5e0820f03245070015fb14b3",
        "field_3448": "SENT",
        "field_3448_raw": "SENT",
        "field_3451": "5b773da5fb0fe322c390274b",
        "field_3451_raw": "5b773da5fb0fe322c390274b",
        "field_3452": '<span class="581602e43285e4a22c90de05">John Clary</span>',
        "field_3452_raw": [
            {"id": "581602e43285e4a22c90de05", "identifier": "John Clary"}
        ],
        "field_3453": "Yes",
        "field_3453_raw": True,
        "field_513": '<span class="5dfa6ac42057600ac95e792e">100 Amp Breaker Panel | EA</span>',
        "field_513_raw": [
            {
                "id": "5dfa6ac42057600ac95e792e",
                "identifier": "100 Amp Breaker Panel | EA",
            }
        ],
        "field_514": '<span class="5df10bf86d76b100157d1003">WRK19-070800</span>',
        "field_514_raw": [
            {"id": "5df10bf86d76b100157d1003", "identifier": "WRK19-070800"}
        ],
        "field_524": "10.00",
        "field_524_raw": 10,
        "field_768": "",
        "field_769": "WORK ORDER",
        "field_769_raw": "WORK ORDER",
        "field_770": 6501,
        "field_770_raw": 6501,
        "field_771": "12/25/2019 22:29",
        "field_771_raw": {
            "am_pm": "PM",
            "date": "12/25/2019",
            "date_formatted": "12/25/2019",
            "hours": "10",
            "iso_timestamp": "2019-12-25T22:29:00.000Z",
            "minutes": "29",
            "time": 1349,
            "timestamp": "12/25/2019 10:29 pm",
            "unix_timestamp": 1577312940000,
        },
        "field_854": "",
        "id": "5e04372f11440400184d79f0",
    }

    # work order
    record = {
        "id": "5df10bf86d76b100157d1003",
        "field_1752": "Yes",
        "field_1752_raw": True,
        "field_458": '<span class="581602e43285e4a22c90de05">John Clary</span>',
        "field_458_raw": [
            {"id": "581602e43285e4a22c90de05", "identifier": "John Clary"}
        ],
        "field_1439": "",
        "field_849": "12/11/2019 9:32am",
        "field_849_raw": {
            "date": "12/11/2019",
            "date_formatted": "12/11/2019",
            "hours": "09",
            "minutes": "32",
            "am_pm": "AM",
            "unix_timestamp": 1576056720000,
            "iso_timestamp": "2019-12-11T09:32:00.000Z",
            "timestamp": "12/11/2019 09:32 am",
            "time": 572,
        },
        "field_2701": 2019,
        "field_2701_raw": 2019,
        "field_2700": 2020,
        "field_2700_raw": 2020,
        "field_1421": '<span class="581602e43285e4a22c90de05">John Clary</span>',
        "field_1421_raw": [
            {"id": "581602e43285e4a22c90de05", "identifier": "John Clary"}
        ],
        "field_1074": "12/11/2019 9:32am",
        "field_1074_raw": {
            "date": "12/11/2019",
            "date_formatted": "12/11/2019",
            "hours": "09",
            "minutes": "32",
            "am_pm": "AM",
            "unix_timestamp": 1576056720000,
            "iso_timestamp": "2019-12-11T09:32:00.000Z",
            "timestamp": "12/11/2019 09:32 am",
            "time": 572,
        },
        "field_1600": "12/11/2019 09:32",
        "field_1600_raw": {
            "date": "12/11/2019",
            "date_formatted": "12/11/2019",
            "hours": "09",
            "minutes": "32",
            "am_pm": "AM",
            "unix_timestamp": 1576056720000,
            "iso_timestamp": "2019-12-11T09:32:00.000Z",
            "timestamp": "12/11/2019 09:32 am",
            "time": 572,
        },
        "field_1599": "",
        "field_968": "TMC",
        "field_968_raw": "TMC",
        "field_977": "Other / No Asset",
        "field_977_raw": "Other / No Asset",
        "field_1004": "Trouble Call",
        "field_1004_raw": "Trouble Call",
        "field_976": "Other",
        "field_976_raw": "Other",
        "field_900": "",
        "field_900_raw": [None],
        "field_1420": "TEST WORK ORDER",
        "field_1420_raw": "TEST WORK ORDER",
        "field_2904": "",
        "field_995": "Other",
        "field_995_raw": "Other",
        "field_1006": "No",
        "field_1006_raw": False,
        "field_460": "",
        "field_460_raw": "",
        "field_463": "",
        "field_463_raw": "",
        "field_1351": "",
        "field_1352": "",
        "field_509": "",
        "field_1007": "",
        "field_1007_raw": "",
        "field_888": "2.00",
        "field_888_raw": 2,
        "field_904": "123 FAKE ST",
        "field_904_raw": "",
        "field_1754": '<span class="581602e43285e4a22c90de05">John Clary</span>',
        "field_1754_raw": [
            {"id": "581602e43285e4a22c90de05", "identifier": "John Clary"}
        ],
        "field_909": "",
        "field_909_raw": [],
        "field_913": 2,
        "field_913_raw": 2,
        "field_969": "",
        "field_1353": "No",
        "field_1353_raw": False,
        "field_1354": "No",
        "field_1354_raw": False,
        "field_1003": "TROUBLE CALL",
        "field_1003_raw": "TROUBLE CALL",
        "field_1008": "Wednesday",
        "field_1008_raw": "Wednesday",
        "field_1187": "John Clary",
        "field_1187_raw": "John Clary",
        "field_1215": "No",
        "field_1215_raw": False,
        "field_1374": "No",
        "field_1374_raw": False,
        "field_455": 14160,
        "field_455_raw": 14160,
        "field_1203": 100070800,
        "field_1203_raw": 100070800,
        "field_1204": "WRK",
        "field_1204_raw": "WRK",
        "field_1205": 2019,
        "field_1205_raw": 2019,
        "field_1206": "19",
        "field_1206_raw": "19",
        "field_1207": "070800",
        "field_1207_raw": "070800",
        "field_1208": "WRK19-070800",
        "field_1208_raw": "WRK19-070800",
        "field_1209": "WRK19-070800",
        "field_1209_raw": "WRK19-070800",
        "field_1069": "Other (John Clary)",
        "field_1069_raw": "Other (John Clary)",
        "field_1235": "",
        "field_1235_raw": [],
        "field_1598": "",
        "field_1839": "No",
        "field_1839_raw": False,
        "field_1060": "",
        "field_1859": "",
        "field_1862": "",
        "field_1863": "",
        "field_1864": "",
        "field_1871": "",
        "field_1962": "",
        "field_1971": "",
        "field_2075": "",
        "field_2074": "",
        "field_2059": "No",
        "field_2059_raw": False,
        "field_1972": "Trouble Call",
        "field_1972_raw": "Trouble Call",
        "field_1973": "",
        "field_1974": "",
        "field_1975": "",
        "field_1975_raw": [None],
        "field_2009": "",
        "field_2079": "",
        "field_2079_raw": "",
        "field_2080": "",
        "field_2080_raw": "",
        "field_2081": "",
        "field_2081_raw": "",
        "field_2082": "",
        "field_2082_raw": "",
        "field_2083": "",
        "field_2083_raw": "",
        "field_2084": "",
        "field_2084_raw": "",
        "field_2078": "",
        "field_2085": "",
        "field_2085_raw": "",
        "field_2086": "",
        "field_2086_raw": "",
        "field_2634": "",
        "field_2634_raw": [],
        "field_2695": 0,
        "field_2695_raw": 0,
        "field_2696": 0,
        "field_2696_raw": 0,
        "field_2690": 1,
        "field_2690_raw": 1,
        "field_2691": 0,
        "field_2691_raw": 0,
        "field_2692": 0,
        "field_2692_raw": 0,
        "field_2693": 0,
        "field_2693_raw": 0,
        "field_2694": 0,
        "field_2694_raw": 0,
        "field_2689": "Assigned",
        "field_2689_raw": "Assigned",
        "field_459": "Assigned",
        "field_459_raw": "Assigned",
        "field_3066": 0,
        "field_3066_raw": 0,
        "field_3067": 0,
        "field_3067_raw": 0,
        "field_3068": 0,
        "field_3068_raw": 0,
        "field_3444": "",
        # "field_3444": "5df63fb5668f810015c601ea",
        "field_3449": "5b422cb82d916c3327423d41",
    }

    # user account
    record = {
        "id": "581602e43285e4a22c90de05",
        "field_167": "John Clary",
        "field_167_raw": {"first": "John", "last": "Clary"},
        "field_168": '<a href="mailto:john.clary@austintexas.gov">fake.clary@austintexas.gov</a>',
        "field_168_raw": {"email": "fakefakefake.clary@austintexas.gov"},
        "field_169": "*********",
        "field_169_raw": "**********",
        "field_170": "active",
        "field_170_raw": "active",
        "field_171": '<span class="profile_10">Asset Editor</span><br /><span class="profile_19">Viewer</span><br /><span class="profile_20">System Administrator</span><br /><span class="profile_24">Program Editor</span><br /><span class="profile_57">Supervisor | AMD</span><br /><span class="profile_65">Technician | AMD</span><br /><span class="profile_68">Quote the of Week Editor</span><br /><span class="profile_76">Inventory Editor</span><br /><span class="profile_97">Account Administrator</span>',
        "field_171_raw": [
            "profile_10",
            "profile_19",
            "profile_20",
            "profile_24",
            "profile_57",
            "profile_65",
            "profile_68",
            "profile_76",
            "profile_97",
        ],
        "field_1502": "Account Administrator, Asset Editor, Inventory Editor, Program Editor, Quote the of Week Editor, Supervisor | AMD, Viewer",
        "field_1502_raw": [
            "Account Administrator",
            "Asset Editor",
            "Inventory Editor",
            "Program Editor",
            "Quote the of Week Editor",
            "Supervisor | AMD",
            "Viewer",
        ],
        "field_2629": "",
        "field_954": "Support Staff",
        "field_954_raw": "Support Staff",
        "field_2590": "(512) 974-3546",
        "field_2590_raw": {
            "formatted": "(512) 974-3546",
            "full": "5129743546",
            "number": "9743546",
            "area": "512",
        },
        "field_1180": "ATD",
        "field_1180_raw": "ATD",
        "field_2186": "ARTERIAL MANAGEMENT",
        "field_2186_raw": "ARTERIAL MANAGEMENT",
        "field_3431": "",
        "field_1231": "01/01/2017",
        "field_1231_raw": {
            "date": "01/01/2017",
            "date_formatted": "01/01/2017",
            "hours": "12",
            "minutes": "00",
            "am_pm": "AM",
            "unix_timestamp": 1483228800000,
            "iso_timestamp": "2017-01-01T00:00:00.000Z",
            "timestamp": "01/01/2017 12:00 am",
            "time": 720,
        },
        "field_1501": '<span class="581602e43285e4a22c90de05">John Clary</span>',
        "field_1501_raw": [
            {"id": "581602e43285e4a22c90de05", "identifier": "John Clary"}
        ],
        "field_1498": "",
        "field_1503": "",
        "field_1504": "",
        "field_2305": "$20.00",
        "field_2305_raw": "20.00",
        "field_2206": "Arterial Management",
        "field_2206_raw": "Arterial Management",
        "field_3446": "5b422cb82d916c3327423d41",
        "field_3446_raw": "5b422cb82d916c3327423d41",
    }

    res = main(
        "5815f29f7f7252cc2ca91c4f",
        "5b422c9b13774837e54ed814",
        record,
        record_type="user_account",
    )
    print(res)
