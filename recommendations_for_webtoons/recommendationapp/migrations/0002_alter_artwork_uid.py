# Generated by Django 4.1.6 on 2023-02-10 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recommendationapp", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="artwork",
            name="uid",
            field=models.CharField(
                blank=True, default="", max_length=20, null=True, unique=True
            ),
        ),
    ]
