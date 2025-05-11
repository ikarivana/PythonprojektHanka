from django import forms
from django.forms import ModelForm

from viewer.models import (
    Pedikura, Rasy, Zdravi, Contact,
    PedikuraReview, ZdraviReview, RasyReview, ContactReview, Image
)

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