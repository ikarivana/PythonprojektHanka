from django.db.transaction import atomic
from django.forms import PasswordInput, NumberInput, DateField, Textarea, CharField
from django.urls import reverse_lazy
from django.views.generic import CreateView

from accounts.models import Profile
from viewer.models import Order
from django.db import transaction

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    phone = forms.CharField(
        label='Telefon',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    date_of_birth = forms.DateField(
        label='Datum narození',
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    biography = forms.CharField(
        label='Biografie',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        labels = {
            'username': 'Uživatelské jméno',
            'first_name': 'Jméno',
            'last_name': 'Příjmení',
            'email': 'Email',
        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['service_date', 'description']

        labels = {
            'servis_date': 'Datum objednání',
            'description': 'Výběr procedůry'
        }
        widgets = {
            'service_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
            'description': forms.Textarea(attrs={'rows': 4}),
        }
