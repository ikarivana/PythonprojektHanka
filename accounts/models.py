from django.db import models
from django.contrib.auth.models import User
from django.db.models import OneToOneField, DateField, TextField, CharField
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = DateField(blank=True, null=True)
    biography = TextField(max_length=500, blank=True)
    phone = CharField(max_length=20, blank=True, null=True)

    class Meta:
        ordering = ['user__username']

    def __str__(self):
        return f"{self.user.username}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
