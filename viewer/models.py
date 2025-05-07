from django.db.models import (
    Model,
    ForeignKey,
    CASCADE,
    SET_NULL,
    DateTimeField,
    IntegerField,
    TextField,
    CharField,
    EmailField
)
from django.contrib.auth.models import User
from accounts.models import Profile

class Pedikura(Model):
    name = CharField(max_length=30, null=False, blank=False, unique=True)
    procedure_time = IntegerField(null=False, blank=False)
    description = TextField(max_length=5000, null=True, blank=True)
    price = IntegerField(null=False, blank=False)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Pedikúra"

    def __repr__(self):
        return f"Pedikura(name={self.name} procedure_time={self.procedure_time} description={self.description} price={self.price})"

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
        return f"Rasy(name={self.name} description={self.description} price={self.price} procedure_time={self.procedure_time})"

    def __str__(self):
        return self.name

class Zdravi(Model):
    name = CharField(max_length=30, null=False, blank=False, unique=True)
    description = TextField(max_length=5000, null=True, blank=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Zdraví"

    def __repr__(self):
        return f"Zdravi(name={self.name} description={self.description})"

    def __str__(self):
        return self.name

class Contact(Model):
    name = CharField(max_length=30, null=False, blank=False, unique=True)
    phone = CharField(max_length=15, null=False, blank=True)
    email = EmailField(null=False, blank=False, unique=True)
    address = TextField(null=False, blank=True)
    description = TextField(max_length=5000, null=True, blank=True)

    def __repr__(self):
        return f"Contact(name={self.name} phone={self.phone} email={self.email} description={self.description} address={self.address})"

    def __str__(self):
        return self.name

class BaseReview(Model):
    user = ForeignKey(User, on_delete=SET_NULL, null=True, blank=False, related_name='%(class)s_reviews')
    rating = IntegerField(null=True, blank=True)
    comment = TextField(max_length=5000, null=True, blank=True)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-updated']

class PedikuraReview(BaseReview):
    pedikura = ForeignKey(Pedikura, on_delete=CASCADE, null=False, blank=False, related_name='reviews')

    @property
    def review(self):
        return self.user

    class Meta:
        ordering = ['-updated']
        unique_together = ['pedikura', 'user']

    def __str__(self):
        return f"{self.review}: {self.pedikura} ({self.rating})"

class RasyReview(BaseReview):
    rasy = ForeignKey(Rasy, on_delete=CASCADE, null=False, blank=False, related_name='reviews')

    @property
    def review(self):
        return self.user

    class Meta:
        ordering = ['-updated']
        unique_together = ['rasy', 'user']

    def __str__(self):
        return f"{self.review}: {self.rasy} ({self.rating})"

class ZdraviReview(BaseReview):
    zdravi = ForeignKey(Zdravi, on_delete=CASCADE, null=False, blank=False, related_name='reviews')

    @property
    def review(self):
        return self.user

    class Meta:
        ordering = ['-updated']
        unique_together = ['zdravi', 'user']

    def __str__(self):
        return f"{self.review}: {self.zdravi} ({self.rating})"

class Order(Model):
    profile = ForeignKey(Profile, on_delete=CASCADE, related_name='orders')
    service_date = DateTimeField("Datum zakázky")
    description = TextField("Popis zakázky", blank=True)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Zakázka"
        verbose_name_plural = "Zakázky"
        ordering = ['-service_date']

    def __str__(self):
        return f"Objednávka pro {self.profile.user.username} na {self.service_date}"
