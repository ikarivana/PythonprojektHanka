
from django import forms
from django.forms import ModelForm
from django.forms.widgets import ClearableFileInput

from .models import Order, Novinky
from viewer.models import (
    Pedikura, Rasy, Zdravi, Contact,
    PedikuraReview, ZdraviReview, RasyReview, ContactReview, Image
)
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['service_date', 'description']
        widgets = {
            'service_date': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control'
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4
                }
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service_date'].required = True
        self.fields['description'].required = True

class BaseReviewForm(forms.ModelForm):
    rating = forms.IntegerField(
        min_value=1,
        max_value=5,
        label='Hodnocení (1-5)',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    comment = forms.CharField(
        label='Komentář',
        required=False,
        widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control'})
    )

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating is not None and (rating < 1 or rating > 5):
            raise forms.ValidationError('Hodnocení musí být mezi 1 a 5')
        return rating

class PedikuraReviewForm(BaseReviewForm):
    class Meta:
        model = PedikuraReview
        fields = ['rating', 'comment']

class ZdraviReviewForm(BaseReviewForm):
    class Meta:
        model = ZdraviReview
        fields = ['rating', 'comment']

class RasyReviewForm(BaseReviewForm):
    class Meta:
        model = RasyReview
        fields = ['rating', 'comment']

class ContactReviewForm(BaseReviewForm):
    class Meta:
         model = ContactReview
         fields = ['rating', 'comment']

         class Meta:
             model = ContactReview
             fields = ['review', 'comment']


class PedikuraModelForm(forms.ModelForm):
    class Meta:
        model = Pedikura
        fields = '__all__'

class RasyModelForm(forms.ModelForm):
    class Meta:
        model = Rasy
        fields = '__all__'

class ZdraviModelForm(forms.ModelForm):
    class Meta:
        model = Zdravi
        fields = '__all__'

class ContactModelForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'

class ImageModelForm(ModelForm):
    class Meta:
        model = Image
        fields = '__all__'


class NovinkyForm(forms.ModelForm):
    def clean_obrazek(self):
        obrazek = self.cleaned_data.get('obrazek')
        if obrazek:
            if obrazek.size > 5*1024*1024:  # 5MB
                raise forms.ValidationError("Obrázek je příliš velký. Maximální velikost je 5MB.")
            # Kontrola typu souboru
            allowed_types = ['image/jpeg', 'image/png', 'image/gif']
            if obrazek.content_type not in allowed_types:
                raise forms.ValidationError("Povolené formáty jsou pouze JPEG, PNG a GIF.")
        return obrazek

    class Meta:
        model = Novinky
        fields = ['titulek', 'obsah', 'obrazek', 'publikovano']
        widgets = {
            'titulek': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Zadejte titulek novinky'
            }),
            'obsah': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Zadejte obsah novinky'
            }),
            'obrazek': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            'publikovano': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        error_messages = {
            'titulek': {
                'required': 'Titulek je povinný.',
                'max_length': 'Titulek je příliš dlouhý.'
            },
            'obsah': {
                'required': 'Obsah je povinný.'
            }
        }
