# Generated by Django 5.0.2 on 2024-02-16 16:45

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("movies", "0003_movie_search_vector_alter_movie_genres"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
CREATE TRIGGER movie_update_search_trigger
BEFORE INSERT OR UPDATE OF title, original_title, search_vector ON movies_movie
FOR EACH ROW EXECUTE PROCEDURE tsvector_update_trigger(
    search_vector, 'pg_catalog.english', title, original_title);
UPDATE movies_movie SET search_vector = NULL;""",
            reverse_sql="DROP TRIGGER IF EXISTS movie_update_search_trigger ON movies_movie;",
        ),
    ]
