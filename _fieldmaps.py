"""
Each entry in the fieldmap dict contains object and field definitions for
translating records across knack applications. Entries are structured like
so:
    - {top-level key} (str): the top-level key of each entry is the type of record
    that the mapping defines. E.g., "inventory_request" or "inventory_txn". The names
    defined here are received from the `record_type` API request parameter.
    
    - objects (dict) : A dict of application names, each with the Knack object ID
        where the records are stored. Each application names is defined in
        `secrets.py`. See `apps` note below.

    - fields (list) : An array of field dictionaries, with the following structure:

        - comment (str): an optional comment documenting the field's purpose.
        
        - directions (list): a list of app-to-app directions for which this field should
            be proceseed. This ensures that only a subset of record fields are sent to the
            destination application, and effictively enforces pre-defined business rules.

            Supported values are `to_data_tracker` and `to_finance_system`.

        - apps (dict): a dicionary of knack application names, as defined in `secrets.py`.
            These follow a standard naming convention, e.g. data_tracker_prod;
            finance_purhasing_prod. We have elected to use app names instead of app_ids,
            because app_ids may change. app_ids are  managed in `secrets.py`.

            Each application entry is a dict which contains field mapping values.

            - id (str) : the field id. If `None`, default value is required

            - transform (str): a transformation function, which is applied on *inbound*
                data. transformation functions are defined in `_transforms.py`

            - default : used to set the default value. required if no field `id` is present.
                ie, this value is set on the destination payload when no src data is 
                provided. it is defined on the `dest` application field definition.

"""
FIELDMAP = {
    "inventory_request": {
        "objects": {
            "finance_purchasing_prod": {"id": "object_25"},
            "data_tracker_prod": {"id": "object_31"},
        },
        "fields": [
            {
                "comment": "The work location name.",
                "directions": ["to_finance_system"],
                "apps": {
                    "finance_purchasing_prod": {"id": "field_576"},
                    "data_tracker_prod": {"id": "field_904"},
                },
            },
            {
                "comment": "The work order id.",
                "directions": ["to_finance_system"],
                "apps": {
                    "finance_purchasing_prod": {"id": "field_766"},
                    "data_tracker_prod": {"id": "field_1209"},
                },
            },
            {
                "comment": "The Knack record ID of the work order in Data Tracker.",
                "directions": ["to_finance_system", "to_data_tracker"],
                "apps": {
                    "finance_purchasing_prod": {"id": "field_767"},
                    "data_tracker_prod": {"id": "id"},
                },
            },
            {
                "comment": "The Knack record ID of the inventory request in the Finance System.",
                "directions": ["to_finance_system", "to_data_tracker"],
                "apps": {
                    "finance_purchasing_prod": {"id": "id"},
                    "data_tracker_prod": {"id": "field_3444"},
                },
            },
            {
                "comment": "The data tracker account ID which created/modified the work order",
                "directions": ["to_finance_system"],
                "apps": {
                    "finance_purchasing_prod": {
                        "id": "field_571",
                        "transform": "text_to_connection",
                    },
                    "data_tracker_prod": {"id": "field_3449"},
                },
            },
            {
                "comment": "Boolean which indicates if the request has been submitted. Always set to true.",
                "directions": ["to_finance_system"],
                "apps": {
                    "finance_purchasing_prod": {"id": "field_649", "default": True},
                    "data_tracker_prod": {"id": None},
                },
            },
        ],
    },
    "inventory_txn": {
        "objects": {
            "finance_purchasing_prod": {"id" : "object_23"},
            "data_tracker_prod": { "id" : "object_36"},
        },
        "fields": [
            {
                "comment": "Boolean which indicates if the item has been issued.",
                "directions": ["to_finance_system", "to_data_tracker"],
                "apps": {
                    "finance_purchasing_prod": {"id": "field_645"},
                    "data_tracker_prod": {"id": "field_2476"},
                },
            },
            {
                "comment": "Account ID of the data tracker user to which the item has been issued.",
                "directions": ["to_data_tracker"],
                "apps": {
                    "finance_purchasing_prod": {"id": "field_792"},
                    "data_tracker_prod": {
                        "id": "field_854",
                        "transform": "text_to_connection",
                    },
                },
            },
            {
                "comment": "Knack record ID of the transaction in the Data Tracker",
                "directions": ["to_finance_system", "to_data_tracker"],
                "apps": {
                    "finance_purchasing_prod": {"id": "field_772"},
                    "data_tracker_prod": {"id": "id"},
                },
            },
            {
                "comment": "item quantity",
                "directions": ["to_finance_system"],
                "apps": {
                    "finance_purchasing_prod": {"id": "field_512"},
                    "data_tracker_prod": {"id": "field_524"},
                },
            },
            {
                "comment": "The Knack record ID of the transaction in the Finance system.",
                "directions": ["to_finance_system", "to_data_tracker"],
                "apps": {
                    "finance_purchasing_prod": {"id": "id"},
                    "data_tracker_prod": {"id": "field_3443"},
                },
            },
            {
                "comment": "Record ID of the inventory request in the finance system.",
                "directions": ["to_finance_system"],
                "apps": {
                    "finance_purchasing_prod": {
                        "id": "field_632",
                        "transform": "text_to_connection",
                    },
                    "data_tracker_prod": {"id": "field_3445"},
                },
            },
            {
                "comment": "The transaction type (work order, return, etc)",
                "directions": ["to_finance_system"],
                "apps": {
                    "finance_purchasing_prod": {"id": "field_509"},
                    "data_tracker_prod": {"id": "field_769"},
                },
            },
            {
                "comment": "The Knack record ID of the inventory item in the finance system",
                "directions": ["to_finance_system"],
                "apps": {
                    "finance_purchasing_prod": {
                        "id": "field_547",
                        "transform": "text_to_connection",
                    },
                    "data_tracker_prod": {"id": "field_3451"},
                },
            },
            {
                "comment": "If the item request is approved by a supervsisor. Always true. A transaction must be approved in the app before a request is triggered.",
                "directions": ["to_finance_system"],
                "apps": {
                    "finance_purchasing_prod": {"id": "field_795", "default": True},
                    "data_tracker_prod": {"id": None},
                },
            },
            {
                "comment": "If the txn record has been sent to the Finance System.",
                "directions": ["to_data_tracker"],
                "apps": {
                    "finance_purchasing_prod": {"id": None},
                    "data_tracker_prod": {"id": "field_3448", "default": True},
                },
            },
        ],
    },
    "user_account": {
        "objects": {
            "finance_purchasing_prod": {"id" : "object_3"},
            "data_tracker_prod": {"id" : "object_9"},
        },
        "fields": [
            {
                "comment": "The Knack record ID of the account in the Data Tracker",
                "directions": ["to_finance_system", "to_data_tracker"],
                "apps": {
                    "finance_purchasing_prod": {"id": "field_791"},
                    "data_tracker_prod": {"id": "id"},
                },
            },
            {
                "comment": "The user's first and last name",
                "directions": ["to_finance_system"],
                "apps": {
                    "finance_purchasing_prod": {"id": "field_4"},
                    "data_tracker_prod": {"id": "field_167_raw"},
                },
            },
            {
                "comment": "The user's email address.",
                "directions": ["to_finance_system"],
                "apps": {
                    "finance_purchasing_prod": {
                        "id": "field_5",
                        "transform": "handle_email",
                    },
                    "data_tracker_prod": {"id": "field_168_raw"},
                },
            },
            {
                "comment": "The users password.",
                "directions": ["to_finance_system"],
                "apps": {
                    "finance_purchasing_prod": {
                        "id": "field_6",
                        "transform": "random_password",
                    },
                    "data_tracker_prod": {"id": "field_169"},
                },
            },
            {
                "comment": "The user's status (active/disabled).",
                "directions": ["to_finance_system"],
                "apps": {
                    "finance_purchasing_prod": {"id": "field_7"},
                    "data_tracker_prod": {"id": "field_170"},
                },
            },
            {
                "comment": "The user's assigned roles. We ignore the source user role and default it to the viewer role in the Finance System.",
                "directions": ["to_finance_system"],
                "apps": {
                    "finance_purchasing_prod": {
                        "id": "field_8",
                        "default": ["profile_27"],
                    },
                    "data_tracker_prod": {"id": None},
                },
            },
            {
                "comment": "The user's business unit/workgroup.",
                "directions": ["to_finance_system"],
                "apps": {
                    "finance_purchasing_prod": {"id": "field_155"},
                    "data_tracker_prod": {"id": "field_2186"},
                },
            },
            {
                "comment": "The Knack record ID of the finance system account",
                "directions": ["to_data_tracker"],
                "apps": {
                    "finance_purchasing_prod": {"id": "id"},
                    "data_tracker_prod": {"id": "field_3446"},
                },
            },
        ],
    },
}