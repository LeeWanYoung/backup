# Generated by Django 4.2.2 on 2023-06-21 01:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("aici", "0003_alter_voc_voc_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="voc",
            name="repair_status",
            field=models.CharField(
                choices=[("수리중", "수리중"), ("수리완료", "수리완료"), ("미수리", "미수리")],
                max_length=100,
            ),
        ),
        migrations.AlterField(
            model_name="voc",
            name="voc_status",
            field=models.CharField(
                choices=[("확인중", "확인중"), ("확인완료", "확인완료"), ("미확인", "미확인")],
                max_length=100,
                null=True,
            ),
        ),
    ]