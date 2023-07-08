# Generated by Django 4.2.2 on 2023-06-21 00:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Gongsa", "0009_post_department"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="agency",
            field=models.CharField(default="", max_length=30, null=True),
        ),
        migrations.AddField(
            model_name="post",
            name="phone",
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name="profile",
            name="agency",
            field=models.CharField(default="", max_length=30),
        ),
        migrations.AddField(
            model_name="profile",
            name="phone",
            field=models.CharField(default="", max_length=20),
        ),
        migrations.AlterField(
            model_name="post",
            name="department",
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name="profile",
            name="department",
            field=models.CharField(max_length=30),
        ),
    ]
