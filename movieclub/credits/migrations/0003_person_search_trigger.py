# Generated by Django 5.0.2 on 2024-02-20 15:31

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("credits", "0002_person_search_vector"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
CREATE TRIGGER person_update_search_trigger
BEFORE INSERT OR UPDATE OF name, search_vector ON credits_person
FOR EACH ROW EXECUTE PROCEDURE tsvector_update_trigger(
    search_vector, 'pg_catalog.english', name);
UPDATE credits_person SET search_vector = NULL;""",
            reverse_sql="DROP TRIGGER IF EXISTS person_update_search_trigger ON credits_person;",
        ),
    ]
