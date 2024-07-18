"""
This module contains the various codecs (encoders and decoders) for the data.
Each codec is self-registering and therefore new codecs can be added by simply creating a new class that inherits from CodecStrategy. 
This makes the system highly extensible whilst remaining DRY, clear and maintainable.
Other potential codecs include XML, XLSX and YAML.
"""

import csv
import io
import json
from datetime import datetime
from decimal import Decimal


class CodecStrategy(type):
    # Class-level list to keep track of subclasses
    subclasses = []

    # Create a list of all the codecs
    names = []
    mime_types = []
    extensions = []

    def __init__(cls, name, bases, class_dict):
        super().__init__(name, bases, class_dict)
        # Register the subclass
        cls.subclasses.append(cls)
        # Register the codec details
        cls.names.append(class_dict["name"])
        cls.mime_types.append(class_dict["mime_type"])
        cls.extensions.append(class_dict["extension"])

    @classmethod
    def get_subclass_from_extension(cls, extension):
        for s in cls.subclasses:
            if s.extension == extension:
                return s

        raise ValueError(f"No codec found for extension '{extension}'.")


class JsonCodec(metaclass=CodecStrategy):

    name = "JSON"
    mime_type = "application/json"
    extension = "json"

    def to_dict(self, data_in):
        return json.loads(data_in)

    def from_dict(self, data_in):
        return json.dumps(data_in, indent=4, default=JsonCodec.json_serial)

    @staticmethod
    def json_serial(obj):
        """JSON serializer for objects not serializable by json dumps"""

        if isinstance(obj, datetime):
            serial = obj.isoformat()
            return serial

        if isinstance(obj, Decimal):
            return float(obj)

        raise TypeError(f"Type {type(obj)} is not serializable by this codec")


class CsvCodec(metaclass=CodecStrategy):

    name = "CSV"
    mime_type = "text/csv"
    extension = "csv"

    def to_dict(self, data_in):
        reader = csv.DictReader(data_in.splitlines())
        data_out = [row for row in reader]
        return data_out

    def from_dict(self, data_in):

        output = io.StringIO()
        fieldnames = data_in[0].keys()

        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()

        for data_dict in data_in:
            writer.writerow(data_dict)

        data_out = output.getvalue()

        output.close()

        return data_out
