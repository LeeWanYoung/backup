# Generated by Django 4.2.2 on 2023-06-20 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Gongsa", "0004_customuser"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="created_at",
            field=models.DateField(auto_now_add=True),
        ),
    ]