from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.db import transaction

from accounts.forms import SignUpForm
from accounts.models import Profile


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
    form_class = SignUpForm
    template_name = 'form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        try:
            with transaction.atomic():
                # Vytvoření uživatele
                user = form.save()

                # Vytvoření profilu
                Profile.objects.create(
                    user=user,
                    phone=form.cleaned_data.get('phone'),
                    date_of_birth=form.cleaned_data.get('date_of_birth'),
                    biography=form.cleaned_data.get('biography')
                )

                # Přihlášení uživatele
                login(self.request, user)

            return redirect(self.success_url)
        except Exception as e:
            print(f"Chyba při registraci: {e}")
            return super().form_invalid(form)

    def form_invalid(self, form):
        print("Chyby ve formuláři:", form.errors)
        return super().form_invalid(form)


def user_logout(request):
    logout(request)
    return redirect(request.META.get('HTTP_REFERER', '/'))