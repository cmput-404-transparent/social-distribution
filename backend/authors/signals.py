from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

Author = get_user_model()

@receiver(post_save, sender=Author)
def create_author_token_and_fields(sender, instance, created, **kwargs):
    if created:
        # Generate a token for the new user
        Token.objects.get_or_create(user=instance)
        
        # Set default values for 'host' and 'page' fields if they are empty
        if not instance.host:
            instance.host = "http://localhost:8000/api/"  # Update this to match your actual host
        if not instance.page:
            instance.page = f"{instance.host}authors/{instance.id}"
        
        instance.save()
