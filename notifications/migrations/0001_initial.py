# Generated by Django 5.1 on 2024-08-27 09:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("habits", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Notification",
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
                ("message", models.TextField()),
                ("sent_at", models.DateTimeField(auto_now_add=True)),
                ("is_sent", models.BooleanField(default=False)),
                (
                    "habit",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="notifications",
                        to="habits.habit",
                    ),
                ),
            ],
            options={
                "ordering": ["-sent_at"],
            },
        ),
    ]
