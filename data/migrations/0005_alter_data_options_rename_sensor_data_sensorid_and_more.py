# Generated by Django 5.0.7 on 2024-07-16 14:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0004_alter_upload_file_hash"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="data",
            options={"verbose_name_plural": "Data"},
        ),
        migrations.RenameField(
            model_name="data",
            old_name="sensor",
            new_name="sensorid",
        ),
        migrations.AlterUniqueTogether(
            name="data",
            unique_together=set(),
        ),
    ]
