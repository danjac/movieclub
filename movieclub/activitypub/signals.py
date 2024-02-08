from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from django.http import HttpRequest

from movieclub.activitypub.models import Actor, Instance
from movieclub.users.models import User


@receiver(user_signed_up, dispatch_uid="users:populate_actor")
def populate_actor(request: HttpRequest, user: User, **kwargs) -> None:
    """Actor added to a new user."""
    try:
        instance = Instance.objects.local().get(domain=request.site.domain)
    except Instance.DoesNotExist:
        return

    Actor.objects.create_for_user(user, instance)
