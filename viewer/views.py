from django.views.generic import *
from django.shortcuts import render
from viewer.models import *
from django.http import HttpResponse


def Home(request):
    return render(request, 'home.html')


class PedicureListView(ListView):
    template_name = 'pedikura.html'
    model = Pedikura
    context_object_name = 'pedicures'


class PedicureDetailView(ListView):
    template_name = 'pedikura.html'
    model = Pedikura
    context_object_name = 'pedicure_detail'


class PedicureCreateView(ListView):
    templates_name = 'pedicure.html'
    model = Pedikura
    context_object_name = 'pedikura_create'


class PedicureUpdateView(ListView):
    templates_name = 'pedikura.html'
    model = Pedikura
    context_object_name = 'pedicure_update'


class PedicureDeleteView(ListView):
    templates_name = 'pedikura.html'
    model = Pedikura
    context_object_name = 'pedicure_delete'




class EyelashListView(ListView):
    template_name = 'rasy.html'
    model = Rasy
    context_object_name = 'eyelashs'


class EyelashDetailView(ListView):
    template_name = 'rasy.html'
    model = Rasy
    context_object_name = 'eyelash_detail'


class EyelashCreateView(ListView):
    templates_name = 'eyelash.html'
    model = Rasy
    context_object_name = 'eyelash_create'


class EyelashUpdateView(ListView):
    templates_name = 'eyelash.html'
    model = Rasy
    context_object_name = 'eyelash_update'


class EyelashDeleteView(ListView):
    templates_name = 'eyelash.html'
    model = Rasy
    context_object_name = 'eyelash_delete'



class HealthListView(ListView):
    template_name = 'zdravi.html'
    model = Zdravi
    context_object_name = 'health'


class HealthDetailView(ListView):
    template_name = 'zdravi.html'
    model = Zdravi
    context_object_name = 'health_detail'


class HealthCreateView(ListView):
    templates_name = 'health.html'
    model = Zdravi
    context_object_name = 'health_create'


class HealthUpdateView(ListView):
    templates_name = 'health.html'
    model = Zdravi
    context_object_name = 'health_update'


class HealthDeleteView(ListView):
    templates_name = 'health.html'
    model = Zdravi
    context_object_name = 'health_delete'


class ContactListView(ListView):
    template_name = 'contact.html'
    model = Contact
    context_object_name = 'contact'


class ContactDetailView(ListView):
    template_name = 'contact.html'
    model = Contact
    context_object_name = 'contact_detail'


class ContactCreateView(ListView):
    templates_name = 'contact.html'
    model = Contact
    context_object_name = 'contact_create'


class ContactUpdateView(ListView):
    templates_name = 'contact.html'
    model = Contact
    context_object_name = 'contact_update'


class ContactDeleteView(ListView):
    templates_name = 'contact.html'
    model = Contact
    context_object_name = 'contact_delete'