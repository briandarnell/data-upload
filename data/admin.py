from django.contrib.admin import ModelAdmin, register

from .models import *


@register(Upload)
class UploadAdmin(ModelAdmin):
    list_display = [
        "id",
        "created_at",
        "updated_at",
        "uploaded_by",
        "file",
        "status",
    ]
    list_editable = ["status"]
    search_fields = ["uploaded_by", "file", "description"]
    list_filter = ["created_at", "updated_at", "status"]
    readonly_fields = ["created_at", "updated_at"]


@register(Data)
class DataAdmin(ModelAdmin):
    list_display = ["timestamp", "sensorid", "temperature", "humidity", "pressure"]
    search_fields = ["timestamp", "sensorid"]
    list_filter = ["timestamp", "sensorid"]
    readonly_fields = ["timestamp", "sensorid", "temperature", "humidity", "pressure"]


@register(FieldMapping)
class FieldMappingAdmin(ModelAdmin):
    list_display = ["name", "mapping"]
    search_fields = ["name", "mapping"]
