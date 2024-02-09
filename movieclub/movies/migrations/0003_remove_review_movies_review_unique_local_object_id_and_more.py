# Generated by Django 5.0.2 on 2024-02-09 14:19

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("activitypub", "0004_rename_activitypub_object_id_follow_object_id_and_more"),
        ("movies", "0002_remove_review_activity_object_id_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="review",
            name="movies_review_unique_local_object_id",
        ),
        migrations.RemoveConstraint(
            model_name="review",
            name="movies_review_unique_remote_object_id",
        ),
        migrations.RenameField(
            model_name="review",
            old_name="activitypub_object_id",
            new_name="object_id",
        ),
        migrations.RemoveField(
            model_name="review",
            name="activitypub_status",
        ),
        migrations.AddField(
            model_name="review",
            name="domain",
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AddConstraint(
            model_name="review",
            constraint=models.UniqueConstraint(
                condition=models.Q(
                    models.Q(("object_id", ""), ("domain", ""), _connector="OR"),
                    _negated=True,
                ),
                fields=("object_id", "domain"),
                name="movies_review_unique_object_id_domain",
            ),
        ),
        migrations.AddConstraint(
            model_name="review",
            constraint=models.UniqueConstraint(
                condition=models.Q(("user__isnull", False)),
                fields=("object_id", "user"),
                name="movies_review_unique_local_object_id",
            ),
        ),
        migrations.AddConstraint(
            model_name="review",
            constraint=models.UniqueConstraint(
                condition=models.Q(("actor__isnull", False)),
                fields=("object_id", "actor"),
                name="movies_review_unique_remote_object_id",
            ),
        ),
    ]
