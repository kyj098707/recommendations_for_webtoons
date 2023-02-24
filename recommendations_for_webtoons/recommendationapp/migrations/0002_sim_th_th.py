# Generated by Django 4.1.6 on 2023-02-21 11:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("recommendationapp", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Sim_th_th",
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
                ("similarity", models.FloatField(default=0, null=True)),
                (
                    "r_artwork1",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="th1_th2",
                        to="recommendationapp.artwork",
                    ),
                ),
                (
                    "r_artwork2",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="th2_th1",
                        to="recommendationapp.artwork",
                    ),
                ),
            ],
            options={
                "ordering": ["similarity"],
            },
        ),
    ]