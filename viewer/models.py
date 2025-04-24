from django.db.models import Model
from django.db.models.fields import *


class Pedikura(Model):
    name = CharField(max_length=30, null=False, blank=False, unique=True)
    procedure_time = IntegerField(null=False, blank=False)
    description = TextField(max_length=5000, null=True, blank=True)
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
    description = TextField(max_length=5000, null=True, blank=True)
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
    description = TextField(max_length=5000, null=True, blank=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Zdraví"

    def __repr__(self):
        return f"Zdravi(name={self.name} descripton={self.descripton})"

    def __str__(self):
        return self.name


class Contact(Model):
    name = CharField(max_length=30, null=False, blank=False, unique=True)
    phone = CharField(max_length=15, null=False, blank=True)
    email = EmailField(null=False, blank=False, unique=True)
    address = TextField(null=False, blank=True)
    description = TextField(max_length=5000, null=True, blank=True)

    def __repr__(self):
        return f"Contacte(name={self.name} phone={self.phone} email={self.email} descripton={self.descripton})"

    def __str__(self):
        return self.name

