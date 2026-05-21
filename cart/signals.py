from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Cart
from accounts.models import CustomUser

@receiver(post_save,sender=CustomUser)
def create_cart_for_user(sender,instance,created,**kwargs):
    if created:
        Cart.objects.create(
            user=instance
        )