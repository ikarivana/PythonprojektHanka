from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import *
from django.shortcuts import render, redirect
from django.contrib import messages
from accounts.models import Profile

from viewer.forms import (
    PedikuraModelForm,
    RasyModelForm,
    ContactModelForm,
    ZdraviModelForm,
    PedikuraReviewForm,
    RasyReviewForm,
    ZdraviReviewForm
)
from viewer.mixins import StaffRequiredMixin
from viewer.models import *
from django.http import HttpResponse
from django.urls import reverse_lazy


def home(request):
    return render(request, 'home.html')

class PedicureListView(ListView):
    template_name = 'pedikura.html'
    model = Pedikura
    context_object_name = 'pedicures'

class PedicureDetailView(DetailView):
    template_name = 'pedicure.html'
    model = Pedikura
    context_object_name = 'pedicure_detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['review_form'] = PedikuraReviewForm()
            context['reviews'] = self.object.reviews.all()
        return context


class PedicureCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'form.html'
    form_class = PedikuraModelForm
    success_url = reverse_lazy('pedicure')
    permission_required = 'viewer.add_pedicure'

    def form_invalid(self, form):
        print("form není validní")
        return super().form_invalid(form)

class PedicureUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'form.html'
    form_class = PedikuraModelForm
    model = Pedikura
    success_url = reverse_lazy('pedicure')
    permission_required = 'viewer.change_pedicure'

    def form_invalid(self, form):
        print("form není validní")
        return super().form_invalid(form)

class PedicureDeleteView(StaffRequiredMixin, PermissionRequiredMixin, DeleteView):
    template_name = 'confirm_delete.html'
    model = Pedikura
    success_url = reverse_lazy('pedicure')
    permission_required = 'viewer.delete_pedicure'



class EyelashListView(ListView):
    template_name = 'rasy.html'
    model = Rasy
    context_object_name = 'eyelashs'

class EyelashDetailView(DetailView):
    template_name = 'eyelash.html'
    model = Rasy
    context_object_name = 'eyelash_detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['review_form'] = RasyModelForm()
            context['reviews'] = self.object.reviews.all()
        return context


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

class HealthDetailView(DetailView):
    template_name = 'health.html'
    model = Zdravi
    context_object_name = 'health_detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['review_form'] = ZdraviModelForm()
            context['reviews'] = self.object.reviews.all()
        return context


class HealthCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'form.html'
    form_class = ZdraviModelForm
    success_url = reverse_lazy('heatlh')
    permission_required = 'viewer.add_zdravi'

    def form_invalid(self, form):
        print("form není validní")
        return super().form_invalid(form)

class HealthUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'form.html'
    model = Zdravi
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

class ContactDetailView(DetailView):
    template_name = 'contacte.html'
    model = Contact
    context_object_name = 'contact_detail'

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


def search(request):
    if request.method == 'POST':
        search_string = request.POST.get('search', '').strip()
        if search_string:
            pedicures_name = Pedikura.objects.filter(pedicure_name__contains=search_string)
            pedicures_description = Pedikura.objects.filter(pedicure_description__contains=search_string)

            eyelash_name = Rasy.objects.filter(eyelash_name__contains=search_string)
            eyelash_description = Rasy.objects.filter(eyelash_description__contains=search_string)

            context = {
                'search': search_string,
                'pedicures_name': pedicures_name,
                'pedicures_description': pedicures_description,
                'eyelash_name': eyelash_name,
                'eyelash_description': eyelash_description
            }


            return render(request, 'search.html', context)
        return render(request, 'home.html')
