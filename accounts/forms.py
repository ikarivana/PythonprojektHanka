from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.transaction import atomic
from django.forms import PasswordInput, NumberInput, DateField, Textarea, CharField

from accounts.models import Profile
from viewer import forms


class SignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'phone', 'date_of_birth']

        labels = {
            'username': 'Uživatelskě jméno',
            'first_name': 'Jméno',
            'last_name': 'Příjmení',
            'email': 'Email',
            'password1': 'Heslo',
            'password2': 'Heslo znovu',
            'phone': 'Phone',
            'date_of_birth': 'Date of Birth',
        }

    password1 = forms.CharField(
        widget=PasswordInput(attrs={'placeholder': 'Heslo'}),
        label='Heslo'
    )
    password2 = forms.CharField(
        widget=PasswordInput(attrs={'placeholder': 'Heslo znovu'}),
        label='Heslo znovu'
    )
    phone = CharField(
        label='Phone',
        required=False
    )
    date_of_birth = DateField(
        widget=NumberInput(attrs={'type': 'date'}),
        label='Datum narození',
        required=False
    )
    biodgraphy = CharField(
        widget=Textarea,
        label='Biografie',
        required=False
    )
    #funkce @atomic hlida pořadi registrace
    @atomic
    def save(self, commit=True):
        self.instance.is_active = True
        user = super().save(commit)

        # vytvoření Profilu uživatele
        date_of_birth = self.cleaned_data.get('date_of_birth')
        biography = self.cleaned_data.get('biodgraphy')
        phone = self.cleaned_data.get('phone')
        profile = Profile(
            user = user,
            date_of_birth = date_of_birth,
            biography = biography,
            phone = phone,
        )
        if commit:
          profile.save()
        return user
