from django.dispatch import receiver
from django.db.models.signals import pre_save
from random import choice
from string import ascii_lowercase, digits
from .models import MyUser





def generate_random_username(length=16, chars=ascii_lowercase+digits, split=4, delimiter='-'):
    username = ''.join([choice(chars) for i in range(length)])
    if split:
        username = delimiter.join([username[start:start+split] for start in range(0, len(username), split)])
    try:
        MyUser.objects.get(username=username)
        return generate_random_username(length=length, chars=chars, split=split, delimiter=delimiter)
    except MyUser.DoesNotExist:
        return username



@receiver(pre_save, sender=MyUser)
def my_callback(sender, instance, *args, **kwargs):
    if instance.pk is None:
        "execute these orders only when first save - created"
        if not(instance.is_superuser):
            instance.username = generate_random_username()


