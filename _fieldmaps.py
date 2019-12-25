"""
Field mappings for translating records across Knack applications.

Each fieldmap contains an array of field dictionaries, with the following structure:

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

        - id (str) : the field id

        - transform (str): a transformation function, which is applied on *inbound*
            data. transformation functions are defined in `_transforms.py`

"""
inventory_request = [
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
        "directions": ["to_finance_system"],
        "apps": {
            "finance_purchasing_prod": {"id": "field_767"},
            "data_tracker_prod": {"id": "id"},
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
]


inventory_txn = [
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
            "data_tracker_prod": {"id": "field_854", "transform": "text_to_connection"},
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
        "directions": ["to_finance_system"],
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
]


user_account = [
    {
        "comment": "The Knack record ID of the account in the Data Tracker",
        "directions": ["to_finance_system"],
        "apps": {
            "finance_purchasing_prod": {
                "id": "TODO",
                "transform": "text_to_connection",
            },
            "data_tracker_prod": {"id": "id"},
        },
    },
    {
        "comment": "The user's first and last name",
        "directions": ["to_finance_system"],
        "apps": {
            "finance_purchasing_prod": {
                "id": "",
                "transform": "TODO-how to populate name fields?",
            },
            "data_tracker_prod": {"id": "field_167"},
        },
    },
    {
        "comment": "The user's email address.",
        "directions": ["to_finance_system"],
        "apps": {
            "finance_purchasing_prod": {"id": "", "transform": "text_to_connection"},
            "data_tracker_prod": {
                "id": "field_168",
                "transform": "TODO-handle email field",
            },
        },
    },
    {
        "comment": "The users password.",
        "directions": ["to_finance_system"],
        "apps": {
            "finance_purchasing_prod": {"id": ""},
            "data_tracker_prod": {"id": "field_169"},
        },
    },
    {
        "comment": "The user's status (active/disabled).",
        "directions": ["to_finance_system"],
        "apps": {
            "finance_purchasing_prod": {"id": ""},
            "data_tracker_prod": {"id": "field_170"},
        },
    },
    {
        "comment": "The user's assigned roles.",
        "directions": ["to_finance_system"],
        "apps": {
            "finance_purchasing_prod": {"id": "", "transform": "TODO"},
            "data_tracker_prod": {"id": "field_171"},
        },
    },
    {
        "comment": "The user's business unit/workgroup.",
        "directions": ["to_finance_system"],
        "apps": {
            "finance_purchasing_prod": {"id": ""},
            "data_tracker_prod": {"id": "field_2186"},
        },
    },
]