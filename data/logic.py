from .codecs import *
from .models import *


def get_latest_upload():

    upload = Upload.objects.last()

    return upload


def process_upload(upload_instance, file):

    upload_data = file.read().decode("utf-8")

    # Get the class of the upload strategy to use
    extension = file.name.split(".")[-1]
    codec_class = CodecStrategy.get_subclass_from_extension(extension)
    codec = codec_class()

    # Use a try-catch block in case of bad data
    # submitted by the user
    # try:
    data_dict = codec.to_dict(upload_data)

    # except Exception as e:
    #    print(e)
    #    return "Data processing failed: " + str(e)

    data_dict_with_mapping = replace_keys_in_list_of_dicts(
        data_dict, upload_instance.field_mapping.mapping
    )
    Data.objects.bulk_create([Data(**d) for d in data_dict_with_mapping])

    upload_instance.status = "processed"

    return "success"


def replace_keys_in_dict(d, mapping):
    return {mapping.get(k, k): v for k, v in d.items()}


def replace_keys_in_list_of_dicts(data, mapping):
    return [replace_keys_in_dict(d, mapping) for d in data]


def check_mappings_exist():
    # Populate the mappings table for the purposes of demonstration
    # In practice, further mappings could be added through the Django admin

    if not FieldMapping.objects.exists():
        FieldMapping.objects.create(
            name="Mapping 1 for Client A",
            mapping={
                "Timestamp": "timestamp",
                "Sensor ID": "sensorid",
                "Temperature": "temperature",
                "Humidity": "humidity",
                "Pressure": "pressure",
            },
        )
