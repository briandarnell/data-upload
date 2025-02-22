# Generated by Django 5.0.7 on 2024-07-16 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0002_rename_json_upload_json_data"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="upload",
            name="json_data",
        ),
        migrations.AddField(
            model_name="upload",
            name="file_hash",
            field=models.CharField(max_length=64, null=True, unique=True),
        ),
        migrations.AddField(
            model_name="upload",
            name="status",
            field=models.CharField(
                choices=[
                    ("pending", "Pending"),
                    ("processed", "Processed"),
                    ("failed", "Failed"),
                ],
                default="pending",
                max_length=10,
            ),
        ),
        migrations.CreateModel(
            name="Data",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("timestamp", models.DateTimeField()),
                ("sensor", models.IntegerField()),
                ("temperature", models.DecimalField(decimal_places=1, max_digits=4)),
                ("humidity", models.DecimalField(decimal_places=1, max_digits=4)),
                ("pressure", models.DecimalField(decimal_places=0, max_digits=4)),
            ],
            options={
                "unique_together": {("timestamp", "sensor")},
            },
        ),
    ]
