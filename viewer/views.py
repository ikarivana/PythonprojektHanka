from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib import messages
from .mixins import StaffRequiredMixin
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.db import models
from viewer.forms import (
    PedikuraModelForm, RasyModelForm, ZdraviModelForm,
    ContactModelForm, PedikuraReviewForm, RasyReviewForm,
    ZdraviReviewForm
)
from viewer.models import Pedikura, Rasy, Zdravi, Contact, Order
from accounts.models import Profile


def home(request):
    print(f"User is authenticated: {request.user.is_authenticated}")
    print(f"User: {request.user}")
    return render(request, 'home.html')


class PedicureListView(ListView):
    template_name = 'pedikura.html'
    model = Pedikura
    context_object_name = 'pedicures'
    permission_required = 'viewer.view_pedikura'
    paginate_by = 2


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


class ContactDetailView(DetailView):
    template_name = 'contacte.html'
    model = Contact
    context_object_name = 'contact_detail'
    permission_required = 'viewer.view_contact'


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
        search_string = request.POST['search'].strip()
        if search_string:
            pedicura_name = Pedikura.objects.filter(name__contains=search_string)
            pedicura_description = Pedikura.objects.filter(description__contains=search_string)
            eyelash_name = Rasy.objects.filter(name__contains=search_string)
            eyelash_description = Rasy.objects.filter(description__contains=search_string)
            health_name = Zdravi.objects.filter(name__contains=search_string)
            health_description = Zdravi.objects.filter(description__contains=search_string)
            contact_name = Contact.objects.filter(name__contains=search_string)

            context = {
                'search': search_string,
                'pedicures': pedicura_name,
                'pedicures_description': pedicura_description,
                'eyelashes': eyelash_name,
                'eyelashes_description': eyelash_description,
                'healths': health_name,
                'healths_description': health_description,
                'contacts': contact_name,
            }
            return render(request, 'search.html', context)
    return render(request, 'home.html')


class OrderListView(LoginRequiredMixin, ListView):
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

