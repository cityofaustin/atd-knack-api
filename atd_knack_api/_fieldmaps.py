# Each entry in the fieldmap dict contains object and field definitions for
# translating records across knack applications. Entries are structured like
# so:
#     - {top-level key} (str): the top-level key of each entry is the type of record
#     that the mapping defines. E.g., "inventory_request" or "inventory_txn". The names
#     defined here are received from the `record_type` API request parameter.
# 
#     - comment (str) : An optional comment that documents the purpose of this record_type.
# 
#     - objects (dict) : A dict of application names, each with the Knack object ID
#         where the records are stored. Each application names is defined in
#         `secrets.py`. See `apps` note below.
# 
#     - fields (list) : An array of field dictionaries, with the following structure:
# 
#         - comment (str): an optional comment documenting the field's purpose.
# 
#         - directions (list): a list of app-to-app directions for which this field should
#             be proceseed. This ensures that only a subset of record fields are sent to the
#             destination application, and effictively enforces pre-defined business rules.
# 
#             Supported values are `to_data_tracker` and `to_finance_system`.
# 
#         - apps (dict): a dicionary of knack application names, as defined in `secrets.py`.
#             These follow a standard naming convention, e.g. data_tracker;
#             finance_purhasing_prod. We have elected to use app names instead of app_ids,
#             because app_ids may change. app_ids are  managed in `secrets.py`.
# 
#             Each application entry is a dict which contains field mapping values.
# 
#             - id (str) : the field id. If `None`, default value is required
# 
#             - transform (str): a transformation function, which is applied on *inbound*
#                 data. transformation functions are defined in `_transforms.py`
# 
#             - default : used to set the default value. required if no field `id` is present.
#                 ie, this value is set on the destination payload when no src data is 
#                 provided. it is defined on the `dest` application field definition.

import os
import yaml

def load_fieldmap(fname):
    with open(fname, "r") as fin:
        return yaml.safe_load(fin.read())

dirname = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(dirname, '_fieldmaps.yml')

FIELDMAP = load_fieldmap(filename)