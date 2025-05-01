from django.contrib.auth.models import User
from django.db import models
from django.db.models import TextField, DateField, OneToOneField, CASCADE, CharField


class Profile(models.Model):
    user = OneToOneField(User, on_delete=CASCADE)
    date_of_birth = DateField(blank=True, null=True)
    biography = TextField(max_length=500, blank=True)
    phone = CharField(max_length=20, blank=True, null=True)

    class Meta:
        ordering = ['user__username']

    def __repr__(self):
        return f"Profil(user={self.user})"

    def __str__(self):
        return self.user.username
