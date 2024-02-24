# Generated by Django 5.0.2 on 2024-02-23 14:31

import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Blogathon",
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
                    "created",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="created",
                    ),
                ),
                (
                    "modified",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="modified",
                    ),
                ),
                ("name", models.CharField(max_length=120)),
                ("starts", models.DateField()),
                ("ends", models.DateField()),
                ("description", models.TextField(blank=True)),
                ("submitted", models.DateTimeField(blank=True, null=True)),
                (
                    "organizer",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="blogathons",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Entry",
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
                    "created",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="created",
                    ),
                ),
                (
                    "modified",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="modified",
                    ),
                ),
                ("blog_title", models.CharField(blank=True, max_length=300)),
                ("blog_url", models.URLField(blank=True)),
                ("blog_summary", models.TextField(blank=True)),
                (
                    "blogathon",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="entries",
                        to="blogathons.blogathon",
                    ),
                ),
                (
                    "participant",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="blogathon_entries",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Proposal",
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
                    "created",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="created",
                    ),
                ),
                (
                    "modified",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="modified",
                    ),
                ),
                (
                    "state",
                    models.CharField(
                        choices=[
                            ("submitted", "Submitted"),
                            ("accepted", "Accepted"),
                            ("rejected", "Rejected"),
                        ],
                        default="submitted",
                        max_length=12,
                    ),
                ),
                ("state_changed_at", models.DateTimeField(blank=True, null=True)),
                ("proposal", models.TextField(blank=True)),
                (
                    "blogathon",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="proposals",
                        to="blogathons.blogathon",
                    ),
                ),
                (
                    "participant",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="blogathon_proposals",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="entry",
            constraint=models.UniqueConstraint(
                fields=("participant", "blogathon"),
                name="blogathons_entry_unique_blogathon_entry",
            ),
        ),
        migrations.AddConstraint(
            model_name="proposal",
            constraint=models.UniqueConstraint(
                condition=models.Q(("state", "submitted")),
                fields=("participant", "blogathon"),
                name="blogathons_proposal_unique_blogathon_proposal",
            ),
        ),
    ]