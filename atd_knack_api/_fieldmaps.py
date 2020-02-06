"""
Each entry in the fieldmap dict contains object and field definitions for
translating records across knack applications. Entries are structured like
so:
    - {top-level key} (str): the top-level key of each entry is the type of record
    that the mapping defines. E.g., "inventory_request" or "inventory_txn". The names
    defined here are received from the `record_type` API request parameter.

    - comment (str) : An optional comment that documents the purpose of this record_type.

    - objects (dict) : A dict of application names, each with the Knack object ID
        where the records are stored. Each application names is defined in
        `secrets.py`. See `apps` note below.

    - fields (list) : An array of field dictionaries, with the following structure:

        - comment (str): an optional comment documenting the field's purpose.

        - directions (list): a list of app-to-app directions for which this field should
            be proceseed. This ensures that only a subset of record fields are sent to the
            destination application, and effictively enforces pre-defined business rules.

            Supported values are `to_data_tracker`,`to_finance_system`, `callback_data_tracker`,
            `callback_finance_system`.

            ABOUT CALLBACKS: The callback direction is used to supply data from the updated/
            created record in the destination app, back to the src application. For example,
            when a transaction record is created in the Finance system, we need to store the
            transaction ID of that record in the Data Tracker, so that the record can be
            further updated. This ensures a link between the corresponding records in each
            system.

            The callback request is always fired at the end of any record handling event. E.g.,
            any time a transaction record is processed, the callback event happens subsequently,
            and the record data provided by the destination API response is transformed according
            to the fieldmap and returned to the src app.

        - apps (dict): a dicionary of knack application names, as defined in `secrets.py`.
            These follow a standard naming convention, e.g. data_tracker;
            finance_purhasing. We have elected to use app names instead of app_ids,
            because app_ids may change. app_ids are  managed in `secrets.py`.

            Each application entry is a dict which contains field mapping values.

            - id (str) : the field id. If `None`, default value is required

            - transform (dict): a transformation function name, which is applied on *src*
                application data to the *dest* application. transformation functions are
                defined in `_transforms.py`. At a minimum, the transform entry needs
                a `name` key, whose value matches that of a transform function defined in
                `transforms.py`.

                THE `LOOKUP` TRANFORM is a special transform function which queries the
                destination application for a record matching a specific field value. This
                mechanism is the means of `linking` records together between the source
                and destination applications. It also the means by which record relationships
                in the source/destination applications are properly populated.
                
                For example, each inventory transaction in the data tracker has a many-to-one
                relationship with the inventory_items object. When a transaction is created
                from the Data Tracker in the Finance System, the same relationship must
                be preserved. In order to achieve this, we must "lookup" the Knack record ID
                of the inventory item record in the finance system, so that we can properly
                set the connection field on the inventory transaction. (As documented
                here: https://www.knack.com/developer-documentation/#set-connection-field)
                
                In the case of inventory items, we use the item's "stock number" which uniquely
                identifies the record in both the Data Tracker and the Finance System, to
                lookup the Knack record ID in each system.
                
                The lookup transform requires additional fields to be specified in the fieldmap.
                    - `config`
                    - `pre_transform`

                Yes, this is all a work around to the fact that Knack primary keys (the `id` field)
                is not directly exposed in the application.

            - default : used to set the default value. required if no field `id` is present.
                ie, this value is set on the destination payload when no src data is 
                provided. it is defined on the `dest` application field definition.
"""
import os
import yaml

def load_fieldmap(fname):
    with open(fname, "r") as fin:
        return yaml.safe_load(fin.read())

dirname = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(dirname, '_fieldmaps.yml')

FIELDMAP = load_fieldmap(filename)