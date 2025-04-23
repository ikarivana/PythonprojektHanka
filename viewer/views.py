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
    templates_name = 'pedikura.html'
    model = Pedikura
    context_object_name = 'pedicure_create'


class PedicureUpdateView(ListView):
    templates_name = 'pedikura.html'
    model = Pedikura
    context_object_name = 'pedicure_update'


class PedicureDeleteView(ListView):
    templates_name = 'pedikura.html'
    model = Pedikura
    context_object_name = 'pedicure_delete'
