from django.apps import AppConfig


class ActivitypubConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "movieclub.activitypub"

    def ready(self) -> None:
        from movieclub.activitypub import signals  # noqa: F401
