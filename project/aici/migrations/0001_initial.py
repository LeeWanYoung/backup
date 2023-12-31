# Generated by Django 4.2.2 on 2023-06-21 01:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="VOC",
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
                ("phone", models.DateField(default=django.utils.timezone.now)),
                ("updated_at", models.DateField(auto_now=True)),
                ("repair_status", models.CharField(max_length=100)),
                ("voc_status", models.DateField(null=True)),
                ("comment", models.TextField(null=True)),
                ("created_at", models.DateField(default=django.utils.timezone.now)),
                (
                    "tt",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
