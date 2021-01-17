from stackoverflow import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance=None, created=False, **kwargs):
    '''function to create profile object'''

    if created:
        # creating profile object with instance of sender(user)
        models.Profile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    '''function to create token object'''

    if created:
        # creating token for instace if sender(user)
        Token.objects.create(user=instance)
