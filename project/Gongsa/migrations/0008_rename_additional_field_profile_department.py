# Generated by Django 4.2.2 on 2023-06-20 08:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("Gongsa", "0007_profile"),
    ]

    operations = [
        migrations.RenameField(
            model_name="profile",
            old_name="additional_field",
            new_name="department",
        ),
    ]
