# Generated by Django 5.0.1 on 2024-02-04 19:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("movies", "0002_review"),
    ]

    operations = [
        migrations.AlterField(
            model_name="review",
            name="comment",
            field=models.TextField(),
        ),
    ]