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

