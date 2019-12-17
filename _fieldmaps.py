work_order_to_inventory_request = [
    {
        "src" : "field_904", # LOCATION_NAME
        "dest" : "field_576" # WORK_LOCATION
    },
    {
        "src" : "field_1209", # ATD_WORK_ORDER_ID
        "dest" : "field_766", # ATD_WORK_ORDER_ID
    },
    {
        "src" : "id", # DATA_TRACKER_RECORD_ID
        "dest" : "field_767", # DATA_TRACKER_RECORD_ID
    },
    {
        "src" : "field_3449", # MODIFIED BY
        "dest" : "field_571" , # CREATED BY
        "transform_dest" : "single_connection"
    },
    {
        "src" : None,
        "dest" : "field_649", # approval needed
        "default" : True
    },
    {
        "src" : None,
        "dest" : "field_653", # waiting for approval
        "default" : 0
    },
    {
        "src" : None,
        "dest" : "field_649", # submitted
        "default" : 1
    },
]


work_order_transactions_to_finance_transactions = [
    # finance account object: object_3
    # work order account object: object_9
    {
        "src" : "field_524", # quantity
        "dest" : "field_512" # quantity
    },
    {
        "src" : "field_3443", # FINANCE_SYSTEM_TXN_RECORD_ID
        "dest" : "id" # FINANCE_SYSTEM_TXN_RECORD_ID
    },
    {
        "src" : "id", # WORK_ORDER_TRANSACTION_ID
        "dest" : "field_772" # WORK_ORDER_TRANSACTION_ID
    },
    {
        "src" : "field_3445", # FINANCE_INVENTORY_REQEUST_ID
        "dest" : "field_632", # inventory_request
        "transform_dest" : "single_connection"
    },
    {
        "src" : None,
        "dest" : "field_509", # REQUEST_TYPE
        "default" : "WORK ORDER"
    },
    {
        "src" : "field_3451", # ITEM_ID_FINANCE_SYSTEM
        "dest" : "field_547", # inventory_item
        "transform_dest" : "single_connection"
    }
]