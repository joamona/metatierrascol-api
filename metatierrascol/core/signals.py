"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def new_user_activation_handler(sender, instance, **kwargs):
    print(instance.username)
"""