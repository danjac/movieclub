# Generated by Django 5.0.2 on 2024-02-24 14:43

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("blogathons", "0002_rename_submitted_blogathon_published_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="proposal",
            old_name="state",
            new_name="status",
        ),
    ]
