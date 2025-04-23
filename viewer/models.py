from django.db.models import Model
from django.db.models.fields import *


class Pedikura(Model):
    name = CharField(max_length=30, null=False, blank=False, unique=True)
    procedure_time = IntegerField(null=False, blank=False)
    descripton = TextField(max_length=1000, null=True, blank=True)
    price = IntegerField(null=False, blank=False)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Pedikúra"

    def __repr__(self):
        return f"Pedikura(name={self.name} procedure_time={self.procedure_time} descripton={self.descripton} price={self.price} )"

    def __str__(self):
        return self.name


class Rasy(Model):
    name = CharField(max_length=30, null=False, blank=False, unique=True)
    procedure_time = IntegerField(null=False, blank=False, default=0)
    descripton = TextField(max_length=1000, null=True, blank=True)
    price = IntegerField(null=False, blank=False)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Řasy"

    def __repr__(self):
        return f"Rasy(name={self.name} descripton={self.descripton} price={self.price})"

    def __str__(self):
        return self.name


class Zdravi(Model):
    name = CharField(max_length=30, null=False, blank=False, unique=True)
    descripton = TextField(max_length=1000, null=True, blank=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Zdraví"

    def __repr__(self):
        return f"Zdravi(name={self.name} descripton={self.descripton})"

    def __str__(self):
        return self.name


class ZdraviContacte(Model):
    name = CharField(max_length=30, null=False, blank=False, unique=True)
    phone = CharField(max_length=15, null=False, blank=False)
    email = EmailField(null=False, blank=False)
    descripton = TextField(max_length=1000, null=True, blank=True)

    def __repr__(self):
        return f"Contacte(name={self.name} phone={self.phone} email={self.email} descripton={self.descripton})"

    def __str__(self):
        return self.name

# Create your models here.
