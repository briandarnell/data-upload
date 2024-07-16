import copy
from json import JSONDecodeError

from django.db.utils import IntegrityError

from .codecs import *
from .models import *


def check_file_is_unique(file_hash):

    if Upload.objects.filter(file_hash=file_hash).exists():
        return False

    return True


def process_upload(upload_instance, file):

    # Make a copy in order to compute hash without changing the file pointer
    # Warning - this could increase memory consumption for large files
    instance_copy = copy.copy(upload_instance)
    file_hash = instance_copy.compute_hash()
    file_is_unique = check_file_is_unique(file_hash)

    if not file_is_unique:
        return f"The file {upload_instance.file.name} has already been uploaded (hash: {file_hash})."

    upload_data = file.read().decode("utf-8")

    # Get the class of the codec to use
    extension = file.name.split(".")[-1]
    codec_class = CodecStrategy.get_subclass_from_extension(extension)
    codec = codec_class()

    # Use a try-catch block in case invalid
    # data is submitted by the user
    try:
        data_dict = codec.to_dict(upload_data)
        data_dict_with_mapping = replace_keys_in_list_of_dicts(
            data_dict, upload_instance.field_mapping.mapping
        )
        Data.objects.bulk_create([Data(**d) for d in data_dict_with_mapping])

    except IntegrityError as e:
        return "Duplicate data entries detected. Timestamp and Sensor ID must be unique together."

    except (ValueError, JSONDecodeError) as e:
        return "A problem was encountered processing the file. Check the file format is valid."

    # TODO: More granular error handling could be implemented over time
    except Exception as e:
        return "Data processing failed: " + str(e)

    upload_instance.status = "processed"

    return "success"


def get_data_for_download(type, mapping_id):

    if type is None:
        type = "json"

    codec_class = CodecStrategy.get_subclass_from_extension(type)
    codec = codec_class()

    if mapping_id is not None:
        mapping = FieldMapping.objects.get(id=mapping_id).mapping
    else:
        # For demonstration purposes, we will just get the first mapping
        # In a production environment, the user might have to select the mapping
        mapping = FieldMapping.objects.first().mapping

    reverse_mapping = {db: file for file, db in mapping.items()}

    field_list = [db for _, db in mapping.items()]

    data = list(Data.objects.all().values(*field_list))
    data_with_mapping = replace_keys_in_list_of_dicts(data, reverse_mapping)

    data_out = codec.from_dict(data_with_mapping)

    return data_out, codec.mime_type, codec.extension


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
