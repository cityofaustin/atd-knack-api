"""
Create an account in the destination app which mirrors an account
in the source app.
"""
from pprint import pprint as print
import pdb

import knackpy

import logging
from _models import RecordMap
from secrets import *


def main(src_app_id, dest_app_id, account):

    auth_data_tracker = KNACK_CREDENTIALS[src_app_id]

    auth_finance_admin = KNACK_CREDENTIALS[dest_app_id]

    print(account)

if __name__ == "__main__":
    import logging
    from _logging import get_logger
    logger = get_logger("_create_account")
    logger.setLevel(logging.DEBUG)
    account = [{'id': '581602e43285e4a22c90de05', 'field_167': 'John Clary', 'field_167_raw': {'first': 'John', 'last': 'Clary'}, 'field_168': '<a href="mailto:john.clary@austintexas.gov">john.clary@austintexas.gov</a>', 'field_168_raw': {'email': 'john.clary@austintexas.gov'}, 'field_169': '*********', 'field_169_raw': '**********', 'field_170': 'active', 'field_170_raw': 'active', 'field_171': '<span class="profile_10">Asset Editor</span><br /><span class="profile_19">Viewer</span><br /><span class="profile_20">System Administrator</span><br /><span class="profile_24">Program Editor</span><br /><span class="profile_57">Supervisor | AMD</span><br /><span class="profile_65">Technician | AMD</span><br /><span class="profile_68">Quote the of Week Editor</span><br /><span class="profile_76">Inventory Editor</span><br /><span class="profile_97">Account Administrator</span>', 'field_171_raw': ['profile_10', 'profile_19', 'profile_20', 'profile_24', 'profile_57', 'profile_65', 'profile_68', 'profile_76', 'profile_97'], 'field_1502': 'Account Administrator, Asset Editor, Inventory Editor, Program Editor, Quote the of Week Editor, Supervisor | AMD, Viewer', 'field_1502_raw': ['Account Administrator', 'Asset Editor', 'Inventory Editor', 'Program Editor', 'Quote the of Week Editor', 'Supervisor | AMD', 'Viewer'], 'field_2629': '', 'field_954': 'Support Staff', 'field_954_raw': 'Support Staff', 'field_2590': '(512) 974-3546', 'field_2590_raw': {'formatted': '(512) 974-3546', 'full': '5129743546', 'number': '9743546', 'area': '512'}, 'field_1180': 'ATD', 'field_1180_raw': 'ATD', 'field_2186': 'ARTERIAL MANAGEMENT', 'field_2186_raw': 'ARTERIAL MANAGEMENT', 'field_3431': '', 'field_1231': '01/01/2017', 'field_1231_raw': {'date': '01/01/2017', 'date_formatted': '01/01/2017', 'hours': '12', 'minutes': '00', 'am_pm': 'AM', 'unix_timestamp': 1483228800000, 'iso_timestamp': '2017-01-01T00:00:00.000Z', 'timestamp': '01/01/2017 12:00 am', 'time': 720}, 'field_1501': '<span class="581602e43285e4a22c90de05">John Clary</span>', 'field_1501_raw': [{'id': '581602e43285e4a22c90de05', 'identifier': 'John Clary'}], 'field_1498': '', 'field_1503': '', 'field_1504': '', 'field_2305': '$20.00', 'field_2305_raw': '20.00', 'field_2206': 'Arterial Management', 'field_2206_raw': 'Arterial Management', 'field_3446': '5b422cb82d916c3327423d41', 'field_3446_raw': '5b422cb82d916c3327423d41'}]
    main("5b422c9b13774837e54ed814", "5815f29f7f7252cc2ca91c4f", account)