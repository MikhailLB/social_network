from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True,verbose_name="О себе")
    photo = models.ImageField(upload_to="users/%Y/%m/%d", default=None, blank=True, null=True, verbose_name='Фото')
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата рождения")

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()