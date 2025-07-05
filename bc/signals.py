from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify

from .models import BusinessCard

User = get_user_model()


def _generate_unique_slug(base_slug: str) -> str:
    slug = base_slug
    counter = 1
    while BusinessCard.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1
    return slug


@receiver(post_save, sender=User)
def create_business_card(sender, instance, created, **kwargs):
    if created:
        base_slug = slugify(instance.username)
        unique_slug = _generate_unique_slug(base_slug)
        BusinessCard.objects.create(user=instance, slug=unique_slug)
