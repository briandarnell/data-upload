import hashlib

from django.db import models


# Abstract model for including common fields applicable to all models:
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# A model for the files uploads
class Upload(BaseModel):
    uploaded_by = models.ForeignKey("auth.User", on_delete=models.CASCADE, null=True)
    # In this demonstration, we store the file on the server
    # In a Production environment, the file would be stored in cloud storage such as AWS S3, Azure Blob, etc.
    file = models.FileField(upload_to="uploads/")
    # To prevent processing duplicate files (allows idempotent uploads)
    file_hash = models.CharField(max_length=64, unique=True)
    field_mapping = models.ForeignKey(
        "FieldMapping", on_delete=models.CASCADE, null=True
    )
    description = models.TextField(blank=True)
    status_choices = [
        ("pending", "Pending"),
        ("processed", "Processed"),
        ("failed", "Failed"),
    ]
    status = models.CharField(max_length=10, choices=status_choices, default="pending")

    def __str__(self):
        return self.file.name

    def save(self, *args, **kwargs):
        if not self.file_hash:
            self.file_hash = self.compute_hash()
        super().save(*args, **kwargs)

    def compute_hash(self):
        hasher = hashlib.sha256()
        for chunk in self.file.chunks():
            hasher.update(chunk)
        self.file.seek(0)
        return hasher.hexdigest()


# A mode to store the data that has been uploaded
class Data(BaseModel):
    timestamp = models.DateTimeField()
    sensorid = models.IntegerField()  # Potentially a foreign key to a Sensor model
    temperature = models.DecimalField(max_digits=4, decimal_places=1)
    humidity = models.DecimalField(max_digits=4, decimal_places=1)
    pressure = models.DecimalField(max_digits=4, decimal_places=0)

    def __str__(self):
        return f"{self.timestamp} - Sensor {self.sensorid}"

    class Meta:
        verbose_name_plural = "Data"

        # To prevent duplicate data points
        unique_together = [["timestamp", "sensorid"]]
        # However, sometimes in the real world, we come across duplicate points that even have different data values
        # Therefore depending on the data cleaning strategy, this constraint may need to be removed


class FieldMapping(BaseModel):
    """In order to allow different field names in the files, mappings can be configured and stored here.
    The format should be a dictionary where the key is the field name in the file and the value is the field name in the Data model.
    e.g. {"Timestamp": "timestamp", "Sensor ID": "sensorid", "Temperature": "temperature", "Hunmidity": "humidity", "Pressure": "pressure"}
    """

    name = models.CharField(max_length=50)
    mapping = models.JSONField(help_text="JSON object with field mappings")

    def __str__(self):
        return self.name


# Other models that might be useful in a production environment
# Client
# Sensor
# Asset/Facility
