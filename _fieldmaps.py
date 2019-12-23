"""
Field mappings for translating records across Knack applications.

Each fieldmap contains an array of field dictionaries, with the following structure:

    - comment (str): an optional comment documenting the field's purpose.
    
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
        "comment" : "The work location name.",
        "apps" : {
            "finance_purchasing_prod" : {
                "id" : "field_576",
            },
            "data_tracker_prod" : {
                    "id" : "field_904",
            }
        }

    },
    {
        "comment" : "The work order id.",
        "apps" : {
            "finance_purchasing_prod" : {
                "id" : "field_766",
            },
            "data_tracker_prod" : {
                "id" : "field_1209",
            }
        }

    },
    {
        "comment" : "The Knack record ID of the work order in Data Tracker.",
        "apps" : {
            "finance_purchasing_prod" : {
                "id" : "field_767",
            },
            "data_tracker_prod" : {
                "id" : "id",
            }
        }

    },
    {
        "comment" : "The data tracker account ID which created/modified the work order",
        "apps" : {
            "finance_purchasing_prod" : {
                "id" : "field_571",
                "transform" : "single_connection"
            },
            "data_tracker_prod" : {
                "id" : "field_3449",
            }
        }

    }
]


inventory_txn = [
    {
        "comment" : "Boolean which indicates if the item has been issued.",
        "apps" : {
            "finance_purchasing_prod" : {
                "id" : "field_645",
            },
            "data_tracker_prod" : {
                "id" : "field_2476",
            }
        }

    },
    {
        "comment" : "Account ID of the data tracker user to which the item has been issued.",
        "apps" : {
            "finance_purchasing_prod" : {
                "id" : "field_792",
            },
            "data_tracker_prod" : {
                "id" : "field_854",
                "transform" : "text_to_connection"
            }
        }
    },
    {
        "comment" : "Knack record ID of the transaction in the Data Tracker",
        "apps" : {
            "finance_purchasing_prod" : {
                "id" : "field_772",
            },
            "data_tracker_prod" : {
                "id" : "id",
            }
        }
    },
   {
        "comment" : "item quantity",
        "apps" : {
            "finance_purchasing_prod" : {
                "id" : "field_512",
            },
            "data_tracker_prod" : {
                "id" : "field_524",
            }
        }
    },
   {
        "comment" : "The Knack record ID of the transaction in the Finance system.",
        "apps" : {
            "finance_purchasing_prod" : {
                "id" : "id",
            },
            "data_tracker_prod" : {
                "id" : "field_3443",
            }
        }
    },

   {
        "comment" : "Record ID of the inventory request in the finance system.",
        "apps" : {
            "finance_purchasing_prod" : {
                "id" : "field_632",
                "transform" : "single_connection"
            },
            "data_tracker_prod" : {
                "id" : "field_3445",
            }
        }
    },
   {
        "comment" : "The transaction type (work order, return, etc)",
        "apps" : {
            "finance_purchasing_prod" : {
                "id" : "field_509",
            },
            "data_tracker_prod" : {
                "id" : "field_769",
            }
        }
    },
   {
        "comment" : "The Knack record ID of the inventory item in the finacne system",
        "apps" : {
            "finance_purchasing_prod" : {
                "id" : "field_547",
                "transform" : "single_connection"
            },
            "data_tracker_prod" : {
                "id" : "field_3451",
            }
        }
    },

]