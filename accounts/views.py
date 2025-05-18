from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView

from .forms import CustomUserCreationForm
from .models import Profile


class SubmittableLoginView(LoginView):
    template_name = 'form.html'

    def form_invalid(self, form):
        try:
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # Vypíšeme debug informace
            print(f"Přihlašovací údaje - username: {username}")
            print(f"Existuje uživatel? {User.objects.filter(username=username).exists()}")

            # Pokus o autentizaci
            user = authenticate(self.request, username=username, password=password)
            print(f"Výsledek autentizace: {user}")

            if not user:
                # Zkontrolujeme, zda uživatel existuje
                try:
                    user_obj = User.objects.get(username=username)
                    print(f"Uživatel existuje v databázi: {user_obj}")
                except User.DoesNotExist:
                    print("Uživatel neexistuje v databázi")

        except Exception as e:
            print(f"Chyba při zpracování formuláře: {e}")

        messages.error(self.request, 'Nesprávné přihlašovací údaje!')
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, 'Úspěšně jste se přihlásili!')
        return super().form_valid(form)


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        try:
            with transaction.atomic():  # Zajistí, že se buď provedou všechny operace, nebo žádná
                print("Začínám registrační proces...")

                # 1. Kontrola existence uživatele
                username = form.cleaned_data.get('username')
                if User.objects.filter(username=username).exists():
                    messages.error(self.request, 'Uživatel s tímto jménem již existuje.')
                    return super().form_invalid(form)

                # 2. Vytvoření uživatele
                user = form.save()
                print(f"Uživatel vytvořen: {user.username}")

                # 3. Bezpečné vytvoření profilu
                if not Profile.objects.filter(user=user).exists():
                    profile = Profile.objects.create(
                        user=user,
                        phone=form.cleaned_data.get('phone'),
                        date_of_birth=form.cleaned_data.get('date_of_birth'),
                        biography=form.cleaned_data.get('biography')
                    )
                    print(f"Profil vytvořen: {profile}")
                else:
                    print("Profil pro tohoto uživatele již existuje")

                # 4. Přihlášení uživatele
                login(self.request, user)
                print("Uživatel přihlášen")

                messages.success(self.request, 'Registrace proběhla úspěšně!')
                return redirect(self.success_url)

        except Exception as e:
            print(f"Chyba při registraci: {str(e)}")
            print(f"Typ chyby: {type(e)}")
            messages.error(self.request, 'Při registraci nastala chyba.')
            return super().form_invalid(form)


def user_logout(request):
    logout(request)
    return redirect(request.META.get('HTTP_REFERER', '/'))

