from typing import re

from django.core.exceptions import ValidationError
from django.forms import CharField, ModelForm, TextInput

from viewer.models import Pedikura, Rasy, Zdravi, Contact


class PedikuraModelForm(ModelForm):
    class Meta:
        model = Pedikura
        fields = '__all__'

        labels = {
            'name': 'Název procedůry',
            'procedure_time': 'Čas procedůry',
            'description': 'Popis',
            'price': 'Cena'
        }

        help_text = {
            'procedure_time': 'Čas v minutách'
        }

        error_messages = {
            'name': {
                'Tento údaj je povinný.'
            }
        }

    name = CharField(max_length=60, required=True, widget=TextInput(attrs={'class': 'bg-info'}),
                     label="Název procedůry")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean_name(self):
        initial = self.cleaned_data['name']
        return initial.capitalize()

    def clean_procedure_time(self):
        initial = self.cleaned_data['procedure_time']
        if initial and initial <= 1:
            raise ValidationError('Délka musí být kladné číslo')
        return initial

    def clean_description(self):
        initial = self.cleaned_data['description']
        sentences = re.sub(r'\s*\.\s*', '.', initial).split('.')
        return '.'.join(sentence.capitalize() for sentence in sentences)

class RasyModelForm(ModelForm):
    class Meta:
        model = Rasy
        fields = '__all__'

        labels = {
            'name': 'Název procedůry',
            'procedure_time': 'Čas procedůry',
            'description': 'Popis',
            'price': 'Cena'
        }

        help_text = {
            'procedure_time': 'Čas v minutách'
        }

        error_messages = {
            'name': {
                'Tento údaj je povinný.'
            }
        }

    name = CharField(max_length=60, required=True, widget=TextInput(attrs={'class': 'bg-info'}),
                     label="Název procedůry")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean_name(self):
        initial = self.cleaned_data['name']
        return initial.capitalize()

    def clean_procedure_time(self):
        initial = self.cleaned_data['procedure_time']
        if initial and initial <= 0:
            raise ValidationError('Délka musí být kladné číslo')
        return initial

    def clean_description(self):
        initial = self.cleaned_data['description']
        sentences = re.sub(r'\s*\.\s*', '.', initial).split('.')
        return '.'.join(sentence.capitalize() for sentence in sentences)



class ZdraviModelForm(ModelForm):
    class Meta:
        model = Zdravi
        fields = '__all__'

        labels = {
            'name': 'Název procedůry',
            'description': 'Popis',
        }

        help_text = {
            'description': 'Informace o produktu'
        }

        error_messages = {
            'name': {
                'Tento údaj je povinný.'
            }
        }

    name = CharField(max_length=60, required=True, widget=TextInput(attrs={'class': 'bg-info'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean_name(self):
        initial = self.cleaned_data['name']
        return initial.capitalize()


class ContactModelForm(ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'

        labels = {
            'name': 'Název procedůry',
            'phone': 'Telefon',
            'description': 'Popis',
            'address': 'Adresa',

        }

        help_text = {
            'name': 'Jméno pracovnice v oblasti péči o tělo',
            'phone': 'Telefoní číslo',
            'address': 'Adresa provozovny - popřípadě i dveře'
        }

        error_messages = {
            'name': {
                'Tento údaj je povinný.'
            }
        }

    name = CharField(max_length=60, required=True, widget=TextInput(attrs={'class': 'bg-info'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean_name(self):
        initial = self.cleaned_data['name']
        return initial.capitalize()
