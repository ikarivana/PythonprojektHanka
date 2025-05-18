from viewer.models import Order
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from datetime import datetime, timedelta
import pytz

class CustomUserCreationForm(UserCreationForm):
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
            'service_date': 'Datum objednání',
            'description': 'Výběr procedury'
        }

        widgets = {
            'service_date': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control',
                    'min': datetime.now().strftime('%Y-%m-%dT%H:%M'),
                    'required': True,
                },
                format='%Y-%m-%dT%H:%M'
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Prosím popište požadovanou proceduru...',
                    'required': True,
                }
            ),
        }

        help_texts = {
            'service_date': 'Vyberte datum a čas vaší návštěvy',
            'description': 'Uveďte detaily o požadované proceduře'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_hour = 8
        self.end_hour = 18

    def clean_service_date(self):
        date = self.cleaned_data.get('service_date')

        if not date:
            raise forms.ValidationError('Datum je povinné pole.')

        now = datetime.now(pytz.UTC)
        if date < now:
            raise forms.ValidationError('Nelze vybrat datum v minulosti.')

        if date.hour < self.start_hour or date.hour >= self.end_hour:
            raise forms.ValidationError(
                f'Objednávky jsou možné pouze mezi {self.start_hour}:00 a {self.end_hour}:00.'
            )

        if date.weekday() >= 5:
            raise forms.ValidationError('O víkendu nepřijímáme objednávky.')

        if date < now + timedelta(hours=24):
            raise forms.ValidationError('Objednávku je nutné vytvořit alespoň 24 hodin předem.')

        return date

    def clean_description(self):
        description = self.cleaned_data.get('description')

        if not description:
            raise forms.ValidationError('Popis procedury je povinný.')

        if len(description.strip()) < 10:
            raise forms.ValidationError('Popis musí obsahovat alespoň 10 znaků.')

        return description.strip()

