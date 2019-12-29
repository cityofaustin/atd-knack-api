from datetime import datetime

from _fieldmaps import fieldmap
import _transforms

class RecordMap(object):
    """
    Generate an inventory request from a work order.
    """
    def __init__(self, src_app_name, dest_app_name, data, record_type=None):

        self.app_name_dest = dest_app_name
        self.app_name_src = src_app_name
        self.data = data
        self.record_type = record_type
        self.fieldmap = fieldmap.get(record_type)

        if not self.fieldmap:
            raise Exception("Cannot find fieldmap. Unknown record `type_` provided.")

        self.direction = self._set_direction()
        self.fields = self.fieldmap.get("fields")
        self.objects = self.fieldmap.get("objects")
        self.payload = self._build_payload()

    def _set_direction(self):
        """
        Determine the fieldmap "direction". This attribute allows the fieldmap to
        properly filter fields
         based on the src/dest applications.
        """
        if "finance" in self.app_name_src.lower():
            direction = "to_data_tracker"

        elif "data_tracker" in self.app_name_src.lower():
            direction = "to_finance_system"
            
        return direction

    def _build_payload(self):
        """
        Map input data to output fields. Fields not definied in `self.fields` are dropped.
        """
        payload = {}

        for field in self.fields:
            
            if self.direction not in field.get("directions"):
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
