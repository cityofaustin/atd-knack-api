from datetime import datetime

import _fieldmaps
import _transforms

class RecordMap(object):
    """
    Generate an inventory request from a work order.
    """
    def __init__(self, data, type_= None):

        self.data = data

        if type_ == "inventory_request":
            self.fieldmap = _fieldmaps.work_order_to_inventory_request
        
        elif type_ == "inventory_transaction":
            self.fieldmap = _fieldmaps.work_order_transactions_to_finance_transactions
        
        elif type_ == "issue_item":
            self.fieldmap = _fieldmaps.finance_txn_to_work_order_txn
        
        else:
            raise Exception("Unspported record type. Choose `inventory_request`, `inventory_transaction`, or `issue_item`.") 

        self.payload = self._build_payload()


    def _build_payload(self):
        """
        Map input data to output fields. 
        """
        payload = {}

        for field in self.fieldmap:
            src_field = field.get("src")
            
            if src_field:
                val = self.data.get(src_field)
                    
                if field.get("transform_dest"):
                    val = self._transform(val, field["transform_dest"])

            else:
                # no source field, use default value
                val = field.get("default")

            payload[field["dest"]] = val

        return payload

    def _transform(self, val, transform):
        transform_func = getattr(_transforms, transform)
        return transform_func(val)




if __name__ == "__main__":
    import logging
    logger = get_logger("_models")
    logger.setLevel(logging.DEBUG)
