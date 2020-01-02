from _fieldmaps import FIELDMAP
import _transforms
from secrets import KNACK_CREDENTIALS


class Record(object):
    """
    Transform a Knack record from a source application to a destination application.
    """

    def __init__(
        self, src_app_name, dest_app_name, data, record_type=None, callback=False
    ):

        self.app_name_dest = dest_app_name
        self.app_name_src = src_app_name
        self.callback = callback
        self.data = data
        self.record_type = record_type
        self.fieldmap = FIELDMAP.get(record_type)

        if not self.fieldmap:
            raise Exception("Cannot find fieldmap. Unknown record `type_` provided.")

        self.direction = self._set_direction()
        self.fields = self.fieldmap.get("fields")
        self.knack_cfg = self.fieldmap.get("knack_cfg")
        self.payload = self._build_payload()
        self.method = self._set_method()

    def _set_direction(self):
        """
        Determine the fieldmap "direction". This attribute allows the fieldmap to
        properly filter fields based on the src/dest applications.
        """
        if self.callback:
            return f"callback_{self.app_name_dest}"

        else:
            return f"to_{self.app_name_dest}"

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

    def _set_method(self):
        """
        Determine if the record will be created or updated in the destination app.
        """
        if self.payload.get("id"):
            return "update"
        else:
            return "create"

    def _transform(self, val, transform):
        transform_func = getattr(_transforms, transform)
        return transform_func(val)

    def send(self):
        """
        Send the record payload to the dest app.
        """
        obj = self.knack_cfg.get(self.dest_app_name).get("object")
        app_id = self.dest
        api_key = KNACK_CREDENTIALS[app_id]["api_key"]
        method = self.method

        res = knackpy.record(
            record, obj_key=obj, app_id=app_id, api_key=api_key, method=method
        )

        return res


if __name__ == "__main__":
    import logging

    logger = get_logger("_models")
    logger.setLevel(logging.DEBUG)
