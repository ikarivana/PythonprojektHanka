import os
from calendar import month
from datetime import datetime
from email.mime import image
from http.client import responses
from django.http import JsonResponse
import requests
from django.template import context
from .models import Image
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib import messages
from .mixins import StaffRequiredMixin
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db import models
from viewer.forms import (
    PedikuraModelForm, RasyModelForm, ZdraviModelForm,
    ContactModelForm, PedikuraReviewForm, RasyReviewForm,
    ZdraviReviewForm, ImageModelForm, ContactReviewForm
)
from viewer.models import Pedikura, Rasy, Zdravi, Contact, Order, Image
from accounts.models import Profile


def home(request):
    home_images = Image.objects.filter(is_home=True)
    print(f"User is authenticated: {request.user.is_authenticated}")
    print(f"User: {request.user}")
    return render(request, 'home.html', {'home_images': home_images})


class PedicureListView(ListView):
    template_name = 'pedikura.html'
    model = Pedikura
    context_object_name = 'pedicures'
    permission_required = 'viewer.view_pedikura'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pedikura1_images'] = Image.objects.filter(pedikura1=True)
        return context


class PedicureDetailView(DetailView):
    template_name = 'pedicure.html'
    model = Pedikura
    context_object_name = 'pedicure_detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Zobrazíme reviews vždy, ale formulář pouze pro přihlášené
        context['reviews'] = self.object.reviews.all()
        if self.request.user.is_authenticated:
            context['review_form'] = PedikuraReviewForm()
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        self.object = self.get_object()
        form = PedikuraReviewForm(request.POST)

        try:
            # Zkusíme najít existující recenzi
            existing_review = self.object.reviews.filter(user=request.user).first()
            if existing_review:
                # Aktualizace existující recenze
                if form.is_valid():
                    existing_review.rating = form.cleaned_data['rating']
                    existing_review.comment = form.cleaned_data['comment']
                    existing_review.save()
                    messages.success(request, 'Vaše hodnocení bylo úspěšně aktualizováno.')
                else:
                    messages.error(request, 'Prosím opravte chyby ve formuláři.')
            else:
                # Vytvoření nové recenze
                if form.is_valid():
                    review = form.save(commit=False)
                    review.pedikura = self.object
                    review.user = request.user
                    review.save()
                    messages.success(request, 'Vaše hodnocení bylo úspěšně přidáno.')
                else:
                    messages.error(request, 'Prosím opravte chyby ve formuláři.')
        except Exception as e:
            messages.error(request, 'Při ukládání hodnocení nastala chyba.')

        return redirect('pedicure_detail', pk=self.object.pk)


class PedicureCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'form.html'
    form_class = PedikuraModelForm
    success_url = reverse_lazy('pedicure')
    permission_required = 'viewer.add_pedikura'

    def form_invalid(self, form):
        print("form není validní")
        return super().form_invalid(form)


class PedicureUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'form.html'
    form_class = PedikuraModelForm
    model = Pedikura
    success_url = reverse_lazy('pedicure')
    permission_required = 'viewer.change_pedikura'
    context_object_name = 'pedicure'

    def form_invalid(self, form):
        print("form není validní")
        return super().form_invalid(form)


class PedicureDeleteView(StaffRequiredMixin, PermissionRequiredMixin, DeleteView):
    template_name = 'confirm_delete.html'
    model = Pedikura
    success_url = reverse_lazy('pedicure')
    permission_required = 'viewer.delete_pedikura'


class EyelashListView(ListView):
    template_name = 'rasy.html'
    model = Rasy
    context_object_name = 'eyelashs'
    permission_required = 'viewer.view_rasy'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rasy1_images'] = Image.objects.filter(rasy1=True)
        return context


class EyelashDetailView(DetailView):
    template_name = 'eyelash.html'
    model = Rasy
    context_object_name = 'eyelash_detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['review_form'] = RasyReviewForm()
            context['reviews'] = self.object.reviews.all()
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        self.object = self.get_object()
        form = RasyReviewForm(request.POST)

        try:
            existing_review = self.object.reviews.filter(user=request.user).first()
            if existing_review:
                # Aktualizace existující recenze
                if form.is_valid():
                    existing_review.rating = form.cleaned_data['rating']
                    existing_review.comment = form.cleaned_data['comment']
                    existing_review.save()
                    messages.success(request, 'Vaše hodnocení bylo úspěšně aktualizováno.')
                else:
                    messages.error(request, 'Prosím opravte chyby ve formuláři.')
            else:
                if form.is_valid():
                    review = form.save(commit=False)
                    review.rasy = self.object
                    review.user = request.user
                    review.save()
                    messages.success(request, 'Vaše hodnocení bylo úspěšně přidáno.')
                else:
                    messages.error(request, 'Prosím opravte chyby ve formuláři.')
        except Exception as e:
            messages.error(request, 'Při ukládání hodnocení nastala chyba.')

        return redirect('eyelash_detail', pk=self.object.pk)


class EyelashCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'form.html'
    form_class = RasyModelForm
    success_url = reverse_lazy('eyelash')
    permission_required = 'viewer.add_rasy'

    def form_invalid(self, form):
        print("form není validní")
        return super().form_invalid(form)


class EyelashUpdateView(PermissionRequiredMixin, UpdateView):
    form_class = RasyModelForm
    template_name = 'form.html'
    model = Rasy
    success_url = reverse_lazy('eyelash')
    permission_required = 'viewer.change_rasy'

    def form_invalid(self, form):
        print("form není validní")
        return super().form_invalid(form)


class EyelashDeleteView(StaffRequiredMixin, PermissionRequiredMixin, DeleteView):
    template_name = 'confirm_delete.html'
    model = Rasy
    success_url = reverse_lazy('eyelash')
    permission_required = 'viewer.delete_rasy'


class HealthListView(ListView):
    template_name = 'zdravi.html'
    model = Zdravi
    context_object_name = 'healths'
    permission_required = 'viewer.view_zdravi'
    zdravi1_images = Image.objects.filter(zdravi1=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['zdravi1_images'] = Image.objects.filter(zdravi1=True)
        return context


class HealthDetailView(DetailView):
    template_name = 'health.html'
    model = Zdravi
    context_object_name = 'health_detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['review_form'] = ZdraviReviewForm()
            context['reviews'] = self.object.reviews.all()
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        self.object = self.get_object()
        form = ZdraviReviewForm(request.POST)

        try:
            existing_review = self.object.reviews.filter(user=request.user).first()
            if existing_review:
                if form.is_valid():
                    existing_review.rating = form.cleaned_data['rating']
                    existing_review.comment = form.cleaned_data['comment']
                    existing_review.save()
                    messages.success(request, 'Vaše hodnocení bylo úspěšně aktualizováno.')
                else:
                    messages.error(request, 'Prosím opravte chyby ve formuláři.')
            else:
                if form.is_valid():
                    review = form.save(commit=False)
                    review.zdravi = self.object
                    review.user = request.user
                    review.save()
                    messages.success(request, 'Vaše hodnocení bylo úspěšně přidáno.')
                else:
                    messages.error(request, 'Prosím opravte chyby ve formuláři.')
        except Exception as e:
            messages.error(request, 'Při ukládání hodnocení nastala chyba.')

        return redirect('health_detail', pk=self.object.pk)


class HealthCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'form.html'
    form_class = ZdraviModelForm
    success_url = reverse_lazy('health')
    permission_required = 'viewer.add_zdravi'

    def form_invalid(self, form):
        print("form není validní")
        return super().form_invalid(form)


class HealthUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'form.html'
    model = Zdravi
    fields = ['name', 'description']
    success_url = reverse_lazy('health')
    permission_required = 'viewer.change_zdravi'

    def form_invalid(self, form):
        print("form není validní")
        return super().form_invalid(form)


class HealthDeleteView(StaffRequiredMixin, PermissionRequiredMixin, DeleteView):
    template_name = 'confirm_delete.html'
    model = Zdravi
    success_url = reverse_lazy('health')
    permission_required = 'viewer.delete_zdravi'


class ContactListView(ListView):
    template_name = 'contact.html'
    model = Contact
    context_object_name = 'contacts'
    permission_required = 'viewer.view_contact'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contact1_images'] = Image.objects.filter(contact1=True)
        return context


class ContactDetailView(DetailView):
    template_name = 'contacte.html'
    model = Contact
    context_object_name = 'contact_detail'
    permission_required = 'viewer.view_contact'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['review_form'] = ContactReviewForm()
            context['reviews'] = self.object.reviews.all()
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        self.object = self.get_object()
        form = ContactReviewForm(request.POST)

        try:
            existing_review = self.object.reviews.filter(user=request.user).first()
            if existing_review:
                if form.is_valid():
                    existing_review.rating = form.cleaned_data['rating']
                    existing_review.comment = form.cleaned_data['comment']
                    existing_review.save()
                    messages.success(request, 'Vaše hodnocení bylo úspěšně aktualizováno.')
                else:
                    messages.error(request, 'Prosím opravte chyby ve formuláři.')
            else:
                if form.is_valid():
                    review = form.save(commit=False)
                    review.contact = self.object
                    review.user = request.user
                    review.save()
                    messages.success(request, 'Vaše hodnocení bylo úspěšně přidáno.')
                else:
                    messages.error(request, 'Prosím opravte chyby ve formuláři.')
        except Exception as e:
            messages.error(request, 'Při ukládání hodnocení nastala chyba.')

        return redirect('contact_detail', pk=self.object.pk)


class ContactCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'form.html'
    form_class = ContactModelForm
    success_url = reverse_lazy('contact')
    permission_required = 'viewer.add_contact'

    def form_invalid(self, form):
        print("form není validní")
        return super().form_invalid(form)


class ContactUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'form.html'
    model = Contact
    form_class = ContactModelForm
    success_url = reverse_lazy('contact')
    permission_required = 'viewer.change_contact'

    def form_invalid(self, form):
        print("form není validní")
        return super().form_invalid(form)


class ContactDeleteView(StaffRequiredMixin, PermissionRequiredMixin, DeleteView):
    template_name = 'confirm_delete.html'
    model = Contact
    success_url = reverse_lazy('contact')
    permission_required = 'viewer.delete_contact'


def search_view(request):
    if request.method == 'POST':
        search_string = request.POST['search'].strip()
        if search_string:
            pedicura_name = Pedikura.objects.filter(name__contains=search_string)
            pedicura_description = Pedikura.objects.filter(description__contains=search_string)
            eyelash_name = Rasy.objects.filter(name__contains=search_string)
            eyelash_description = Rasy.objects.filter(description__contains=search_string)
            health_name = Zdravi.objects.filter(name__contains=search_string)
            health_description = Zdravi.objects.filter(description__contains=search_string)
            contact_name = Contact.objects.filter(name__contains=search_string)

            url = (f"https://www.googleapis.com/customsearch/v1"
                   f"?key={os.getenv('GOOGLE_API_KEY')}"
                   f"&cx={os.getenv('GOOGLE_CX')}"
                   F"&q={search_string}")
            g_request = requests.get(url)
            print(f"g_request: {g_request}")
            g_json = g_request.json()
            print(f"g_jeson: {g_json}")
            for g_result in g_json:
                print(g_result)
                print(f"\t{g_result}")

            context = {
                'search': search_string,
                'pedicures': pedicura_name,
                'pedicures_description': pedicura_description,
                'eyelashes': eyelash_name,
                'eyelashes_description': eyelash_description,
                'healths': health_name,
                'healths_description': health_description,
                'contacts': contact_name
            }
            return render(request, 'search.html', context)

            # Požadavky GET nebo prázdné vyhledávání, vypíše šablonu s prazdným kontexem.
            context = {
                'search': '',
                'pedicures': Pedikura.objects.none(),
                'pedicures_description': Pedikura.objects.none(),
                'eyelashes': Rasy.objects.none(),
                'eyelashes_description': Rasy.objects.none(),
                'healths': Zdravi.objects.none(),
                'healths_description': Zdravi.objects.none(),
                'contacts': Contact.objects.none(),
            }
    return render(request, 'search.html', context)


class OrderListView(LoginRequiredMixin, ListView):
    order_images = Image.objects.filter(order=True)
    model = Order
    template_name = 'order_list.html'
    context_object_name = 'orders'
    paginate_by = 10

    def get_queryset(self):
        return Order.objects.filter(profile=self.request.user.profile)


class OrderCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Order
    template_name = 'form.html'
    fields = ['service_date', 'description']
    success_url = reverse_lazy('order-list')

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        form.instance.profile = self.request.user.profile
        return super().form_valid(form)


class ImageListView(ListView):
    template_name = 'images.html'
    model = Image
    context_object_name = 'images'
    paginate_by = 5

    def images(request):
        images = Image.objects.all()
        return render(request, 'images.html', {'images': images})

    def images_view(request):
        pedikura_images = Image.objects.filter(pedikura=True)
        rasy_images = Image.objects.filter(rasy=True)
        zdravi_images = Images.objects.filter(zdravi=True)
        contact_images = Images.objects.filter(contact=True)
        home_images = Images.objects.filter(is_home=True)
        order_images = Images.objects.filter(order=True)
        pedikura1_images = Images.objects.filter(pedikura1=True)
        rasy1_images = Images.objects.filter(rasy1=True)
        zdravi1_images = Images.objects.filter(zdravi1=True)
        contact1_images = Images.objects.filter(contact1=True)

        return render(request, 'images.html',
                      {'pedikura_images': pedikura_images, 'rasy_images': rasy_images, 'zdravi_images': zdravi_images,
                       'contact_images': contact_images, 'home_images': home_images, 'order_images': order_images,
                       'pedikura1': pedikura1_images, 'rasy1': rasy1_images, 'zdravi1': zdravi1_images,
                       'contact1': contact1_images})


class ImageDetailView(DetailView):
    template_name = 'image.html'
    model = Image
    def image_detail(request, pk):
        get_object_or_404(Image, id=id)
        return render(request, 'image.html', {'image': image})


class ImageCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'form_image.html'
    form_class = ImageModelForm
    success_url = reverse_lazy('images')
    permission_required = 'viewer.add_image'


class ImageUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'form_image.html'
    model = Image
    form_class = ImageModelForm
    success_url = reverse_lazy('images')
    permission_required = 'viewer.change_image'


class ImageDeleteView(StaffRequiredMixin, PermissionRequiredMixin, DeleteView):
    template_name = 'confirm_delete.html'
    model = Image
    success_url = reverse_lazy('images')
    permission_required = 'viewer.delete_image'


def name_day(request):
    try:
        # Získání dnešního data ve formátu DDMM
        today = datetime.now().strftime("%d%m")
        api_url = f"https://svatky.adresa.info/json?lang=cs&date={today}"

        # HTTP požadavek s timeoutem a ošetřením chyb
        response = requests.get(api_url, timeout=5)
        response.raise_for_status()
        result_json = response.json()
        if isinstance(result_json, list) and len(result_json) > 0:
            name = result_json[0].get('name', 'Neznámé jméno')
        else:
            name = "Dnes nikdo nemá svátek"

    except requests.exceptions.RequestException as e:
        print(f"Chyba při komunikaci s API: {e}")
        name = "Nelze zjistit svátek"

    except (ValueError, KeyError) as e:
        print(f"Chyba při parsování JSON: {e}")
        name = "Chyba v datech"

    return render(request, 'svatek.html', {'name': name})
