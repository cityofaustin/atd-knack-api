from datetime import datetime

import _fieldmaps
import _transforms

class RecordMap(object):
    """
    Generate an inventory request from a work order.
    """
    def __init__(self, src_app_name, dest_app_name, data, direction=None, type_= None):

        
        self.app_name_dest = dest_app_name
        self.app_name_src = src_app_name
        self.data = data
        self.dir = direction
        self.type = type_

        if self.type  == "inventory_request":
            self.fieldmap = _fieldmaps.inventory_request
        
        elif self.type  == "inventory_txn":
            self.fieldmap = _fieldmaps.inventory_txn
        
        else:
            raise Exception("Unspported record type. Choose `inventory_request`, `inventory_txn`, or `issue_item`.") 

        self.payload = self._build_payload()


    def _build_payload(self):
        """
        Map input data to output fields. Fields not definied in `_fieldmaps` are dropped.
        """
        payload = {}

        for field in self.fieldmap:
            
            if self.dir not in field.get("directions"):
                # ignore fields that do not support the direction of data flow
                continue

            src_field_id = field.get("apps").get(self.app_name_src).get("id")
            
            dest_field_id = field.get("apps").get(self.app_name_dest).get("id")

            transform = field.get("apps").get(self.app_name_dest).get("transform")

            if not src_field_id:
                # field is not present in src data; use default value.
                val = field.get("apps").get(self.app_name_dest).get("default")
            
            else:
                val = self.data.get(src_field_id)

            if transform:
                val = self._transform(val, transform)

            payload[dest_field_id] = val

        return payload

    def _transform(self, val, transform):
        transform_func = getattr(_transforms, transform)
        return transform_func(val)




if __name__ == "__main__":
    import logging
    logger = get_logger("_models")
    logger.setLevel(logging.DEBUG)
