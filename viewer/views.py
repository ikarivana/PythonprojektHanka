from django.views.generic import *
from django.shortcuts import render


from viewer.forms import PedikuraModelForm, RasyModelForm, ContactModelForm, ZdraviModelForm
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

class PedicureCreateView(CreateView):
    template_name = 'form.html'
    form_class = PedikuraModelForm
    success_url = reverse_lazy('pedicure')

    def form_invalid(self, form):
        print("form není validní")
        return super().form_invalid(form)

class PedicureUpdateView(UpdateView):
    template_name = 'form.html'
    form_class = PedikuraModelForm
    model = Pedikura
    success_url = reverse_lazy('pedicure')

    def form_invalid(self, form):
        print("form není validní")
        return super().form_invalid(form)

class PedicureDeleteView(DeleteView):
    template_name = 'confirm_delete.html'
    model = Pedikura
    success_url = reverse_lazy('pedicure')




class EyelashListView(ListView):
    template_name = 'rasy.html'
    model = Rasy
    context_object_name = 'eyelashs'

class EyelashDetailView(DetailView):
    template_name = 'eyelash.html'
    model = Rasy
    context_object_name = 'eyelash_detail'

class EyelashCreateView(CreateView):
    template_name = 'form.html'
    form_class = RasyModelForm
    success_url = reverse_lazy('eyelash')

    def form_invalid(self, form):
        print("form není validní")
        return super().form_invalid(form)

class EyelashUpdateView(UpdateView):
    form_class = RasyModelForm
    template_name = 'form.html'
    model = Rasy
    success_url = reverse_lazy('eyelash')

    def form_invalid(self, form):
        print("form není validní")
        return super().form_invalid(form)

class EyelashDeleteView(DeleteView):
    templates_name = 'confirm_delete.html'
    model = Rasy
    success_url = reverse_lazy('eyelash')



class HealthListView(ListView):
    template_name = 'zdravi.html'
    model = Zdravi
    context_object_name = 'healths'

class HealthDetailView(DetailView):
    template_name = 'health.html'
    model = Zdravi
    context_object_name = 'health_detail'

class HealthCreateView(CreateView):
    template_name = 'form.html'
    form_class = ZdraviModelForm
    success_url = reverse_lazy('heatlh')

    def form_invalid(self, form):
        print("form není validní")
        return super().form_invalid(form)

class HealthUpdateView(UpdateView):
    template_name = 'form.html'
    model = Zdravi
    success_url = reverse_lazy('health')

    def form_invalid(self, form):
        print("form není validní")
        return super().form_invalid(form)

class HealthDeleteView(DeleteView):
    template_name = 'confirm_delete.html'
    model = Zdravi
    success_url = reverse_lazy('health')



class ContactListView(ListView):
    template_name = 'contact.html'
    model = Contact
    context_object_name = 'contacts'

class ContactDetailView(DetailView):
    template_name = 'contacte.html'
    model = Contact
    context_object_name = 'contact_detail'

class ContactCreateView(CreateView):
    template_name = 'form.html'
    form_class = ContactModelForm
    success_url = reverse_lazy('contact')

    def form_invalid(self, form):
        print("form není validní")
        return super().form_invalid(form)

class ContactUpdateView(UpdateView):
    template_name = 'form.html'
    model = Contact
    success_url = reverse_lazy('contact')

    def form_invalid(self, form):
        print("form není validní")
        return super().form_invalid(form)

class ContactDeleteView(DeleteView):
    template_name = 'confirm_delete.html'
    model = Contact
    success_url = reverse_lazy('contact')


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
