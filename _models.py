from datetime import datetime

import _fieldmaps
import _transforms

class InventoryRequest(object):
    """
    Generate an inventory request from a work order.
    """

    def __init__(self, data):

        self.data = data

        self.fieldmap = _fieldmaps.work_order_to_inventory_request

        self.payload = self._build_payload()


    def _build_payload(self):

        payload = {}

        for field in self.fieldmap:
            src_field = field.get("src")
            
            if src_field:
                val = self.data.get(src_field)
                    
                if field.get("transform_dest"):
                    val = self._transform(val, field["transform_dest"])

            else:
                # no source field, use default
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
