from datetime import datetime

import _fieldmaps
import _transforms

class RecordMap(object):
    """
    Generate an inventory request from a work order.
    """
    def __init__(self, src, dest, data, direction=None, type_= None):

        self.data = data
        self.dest = dest
        self.dir = direction
        self.src = src
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

            src_field_id = field.get("apps").get(self.src).get("id")
            
            dest_field_id = field.get("apps").get(self.dest).get("id")

            transform = field.get("apps").get(self.dest).get("transform")

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
