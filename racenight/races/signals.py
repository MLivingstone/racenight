from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Race

@receiver(post_save, sender=Race)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    print(f'Status {sender.status}')
    print('Race saved')