# Generated by Django 4.1.6 on 2023-02-10 10:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Detail",
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
                ("title_id", models.CharField(blank=True, max_length=15, null=True)),
                ("title", models.CharField(blank=True, max_length=20, null=True)),
                ("website", models.CharField(blank=True, max_length=10, null=True)),
                ("story", models.TextField(blank=True, null=True)),
            ],
            options={
                "db_table": "detail",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Artist",
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
                (
                    "name",
                    models.CharField(blank=True, default="", max_length=255, null=True),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Artwork",
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
                (
                    "uid",
                    models.CharField(blank=True, default="", max_length=20, null=True),
                ),
                ("star", models.FloatField(blank=True, default=0, null=True)),
                (
                    "title",
                    models.CharField(blank=True, default="", max_length=255, null=True),
                ),
                (
                    "artist",
                    models.CharField(blank=True, default="", max_length=100, null=True),
                ),
                ("story", models.TextField(blank=True, default="", null=True)),
                ("url", models.TextField(blank=True, default="", null=True)),
                (
                    "path_thumb",
                    models.CharField(blank=True, default="", max_length=255, null=True),
                ),
                ("enable", models.BooleanField(default=True)),
            ],
            options={
                "ordering": ["title"],
            },
        ),
        migrations.CreateModel(
            name="Genre",
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
                ("name", models.CharField(default="", max_length=255, null=True)),
                ("count", models.IntegerField(blank=True, default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Publisher",
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
                (
                    "name",
                    models.CharField(blank=True, default="", max_length=255, null=True),
                ),
                ("count", models.IntegerField(blank=True, default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Sim_st_st",
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
                        related_name="st1_st2",
                        to="recommendationapp.artwork",
                    ),
                ),
                (
                    "r_artwork2",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="st2_st1",
                        to="recommendationapp.artwork",
                    ),
                ),
            ],
            options={
                "ordering": ["similarity"],
            },
        ),
        migrations.CreateModel(
            name="Rel_gr_aw",
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
                (
                    "r_artwork",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="aw_gr",
                        to="recommendationapp.artwork",
                    ),
                ),
                (
                    "r_genre",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="gr_aw",
                        to="recommendationapp.genre",
                    ),
                ),
            ],
            options={
                "ordering": ["r_artwork__title"],
            },
        ),
        migrations.CreateModel(
            name="Rel_ar_aw",
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
                (
                    "type",
                    models.CharField(blank=True, default="", max_length=255, null=True),
                ),
                (
                    "r_artist",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="ar_aw",
                        to="recommendationapp.artist",
                    ),
                ),
                (
                    "r_artwork",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="aw_ar",
                        to="recommendationapp.artwork",
                    ),
                ),
            ],
            options={
                "ordering": ["r_artist__name", "r_artwork__title", "type"],
            },
        ),
        migrations.AddField(
            model_name="artwork",
            name="genre",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="genre",
                to="recommendationapp.genre",
            ),
        ),
        migrations.AddField(
            model_name="artwork",
            name="publisher",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="publish",
                to="recommendationapp.publisher",
            ),
        ),
    ]
