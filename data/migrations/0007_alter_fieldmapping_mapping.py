# Generated by Django 5.0.7 on 2024-07-16 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0006_fieldmapping_upload_field_mapping"),
    ]

    operations = [
        migrations.AlterField(
            model_name="fieldmapping",
            name="mapping",
            field=models.JSONField(help_text="JSON object with field mappings"),
        ),
    ]
