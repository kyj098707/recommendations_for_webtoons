# Generated by Django 4.1.6 on 2023-02-24 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "recommendationapp",
            "0004_member_remove_user_passwrod_remove_user_userprofile_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="member",
            name="uid",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
