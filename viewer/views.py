import os
from datetime import datetime
from email.mime import image
import requests
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, permission_required

from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin
)
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
    CreateView
)

from accounts.forms import CustomUserCreationForm
from .forms import OrderForm, NovinkyForm

from accounts.models import Profile
from viewer.forms import (
    PedikuraModelForm,
    RasyModelForm,
    ZdraviModelForm,
    ContactModelForm,
    PedikuraReviewForm,
    RasyReviewForm,
    ZdraviReviewForm,
    ImageModelForm,
    ContactReviewForm
)
from viewer.models import (
    Pedikura,
    Rasy,
    Zdravi,
    Contact,
    Order,
    Image,
    Novinky,
    NovinkyImage,
    PedikuraReview,
    RasyReview,
    ZdraviReview,
    ContactReview
)
from .mixins import StaffRequiredMixin


def home(request):
    try:
        home_images = Image.objects.filter(is_home=True)
        context = {
            'home_images': home_images,
            'welcome_message': 'Vítejte na našich stránkách'
        }

        if request.user.is_authenticated:
            display_name = request.user.get_full_name() or request.user.username
            context['welcome_message'] = f'Vítejte, {display_name}! Zdraví v každém kroku'
            context.update({
                'is_staff': request.user.is_staff,
                'last_login': request.user.last_login,
            })

        return render(request, 'home.html', context)
    except Exception as e:
        messages.error(request, f"Nastala chyba při načítání stránky: {str(e)}")
        return render(request, 'home.html', {'welcome_message': 'Vítejte na našich stránkách'})


# Zabezpečení pro class-based views
class ImageCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'  # přesměrování nepřihlášení uživatele
    model = Image
    fields = ['image', 'is_home', 'pedikura1', 'rasy1', 'zdravi1', 'contact1']


class ImageUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    model = Image
    fields = ['image', 'is_home', 'pedikura1', 'rasy1', 'zdravi1', 'contact1']


class ImageDeleteView(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    model = Image
    success_url = reverse_lazy('home')


class PedicureListView(ListView):
    template_name = 'pedikura.html'
    model = Pedikura
    context_object_name = 'pedicures'
    permission_required = 'viewer.view_pedikura'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pedikura1_images'] = Image.objects.filter(pedikura1=True)
        if not self.request.user.is_authenticated:
            context['registration_form'] = CustomUserCreationForm()
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                messages.success(request, 'Registrace proběhla úspěšně!')
                return redirect('pedicure')
            else:
                self.object_list = self.get_queryset()
                context = self.get_context_data(registration_form=form)
                return self.render_to_response(context)
        return redirect('pedicure')


class PedicureDetailView(DetailView):
    template_name = 'pedicure.html'
    model = Pedikura
    context_object_name = 'pedicure_detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = self.object.reviews.all()
        if self.request.user.is_authenticated:
            context['review_form'] = PedikuraReviewForm()
        else:
            context['registration_form'] = CustomUserCreationForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if not request.user.is_authenticated:
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                messages.success(request, 'Registrace proběhla úspěšně!')
                return redirect('pedicure_detail', pk=self.object.pk)
            else:
                context = self.get_context_data(registration_form=form)
                return self.render_to_response(context)

        # Existující logika pro hodnocení
        form = PedikuraReviewForm(request.POST)
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
        # Recenze zobrazujeme všem
        context['reviews'] = self.object.reviews.all()
        # Formulář pouze přihlášeným
        if self.request.user.is_authenticated:
            context['review_form'] = RasyReviewForm()
        else:
            context['registration_form'] = CustomUserCreationForm()
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
        # Přidáme recenze pro všechny uživatele
        context['reviews'] = self.object.reviews.all()
        # Formulář pro recenze pouze pro přihlášené
        if self.request.user.is_authenticated:
            context['review_form'] = ZdraviReviewForm()
        else:
            context['registration_form'] = CustomUserCreationForm()
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
        # Recenze pro všechny, seřazené od nejnovější
        context['reviews'] = self.object.reviews.all().order_by('-created')
        # Formulář pouze pro přihlášené
        if self.request.user.is_authenticated:
            context['review_form'] = ContactReviewForm()
        else:
            context['registration_form'] = CustomUserCreationForm()
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
                   f"&q={search_string}")
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
        else:
            # Prázdný vyhledávací řetězec
            context = {
                'search': '',
                'pedicures': Pedikura.objects.none(),
                'pedicures_description': Pedikura.objects.none(),
                'eyelashes': Rasy.objects.none(),
                'eyelashes_description': Rasy.objects.none(),
                'healths': Zdravi.objects.none(),
                'healths_description': Zdravi.objects.none(),
                'contacts': Contact.objects.none()
            }
    else:
        # GET požadavek
        context = {
            'search': '',
            'pedicures': Pedikura.objects.none(),
            'pedicures_description': Pedikura.objects.none(),
            'eyelashes': Rasy.objects.none(),
            'eyelashes_description': Rasy.objects.none(),
            'healths': Zdravi.objects.none(),
            'healths_description': Zdravi.objects.none(),
            'contacts': Contact.objects.none()
        }

    return render(request, 'search.html', context)


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        # Kontrola existence profilu
        try:
            profile = self.request.user.profile
        except Profile.DoesNotExist:
            profile = Profile.objects.create(user=self.request.user)

        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(profile=profile)


class OrderCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'form.html'
    success_url = reverse_lazy('viewer:order-list')

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        form.instance.profile = self.request.user.profile
        messages.success(self.request, 'Objednávka byla úspěšně vytvořena.')
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
        zdravi_images = Image.objects.filter(zdravi=True)
        contact_images = Image.objects.filter(contact=True)
        home_images = Image.objects.filter(is_home=True)
        order_images = Image.objects.filter(order=True)
        pedikura1_images = Image.objects.filter(pedikura1=True)
        rasy1_images = Image.objects.filter(rasy1=True)
        zdravi1_images = Image.objects.filter(zdravi1=True)
        contact1_images = Image.objects.filter(contact1=True)

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
    permission_required = 'viewer.add_image'

    def form_valid(self, form):
        contact_id = self.request.GET.get('contact_id')
        if contact_id:
            form.instance.contact_id = contact_id
        return super().form_valid(form)

    def get_success_url(self):
        contact_id = self.request.GET.get('contact_id')
        if contact_id:
            return reverse_lazy('contact_detail', kwargs={'pk': contact_id})
        next_url = self.request.POST.get('next') or self.request.GET.get('next')
        if next_url:
            return next_url
        return reverse_lazy('images')


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


def seznam_novinek(request):
    if request.user.is_authenticated and request.user.has_perm('viewer.add_novinky'):
        if request.method == 'POST':
            form = NovinkyForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    novinka = form.save(commit=False)
                    novinka.autor = request.user
                    novinka.save()

                    # Zpracování dalších obrázků
                    for image in request.FILES.getlist('images'):
                        if image.size <= 5 * 1024 * 1024:  # 5MB limit
                            NovinkyImage.objects.create(
                                novinka=novinka,
                                image=image
                            )
                        else:
                            messages.warning(request, f'Obrázek {image.name} byl přeskočen - je větší než 5MB.')

                    messages.success(request, 'Novinka byla úspěšně vytvořena!')
                    return redirect('seznam_novinek')
                except Exception as e:
                    messages.error(request, f'Při ukládání došlo k chybě: {str(e)}')
            else:
                messages.error(request, 'Prosím opravte chyby ve formuláři.')
        else:
            form = NovinkyForm()
    else:
        form = None

    novinky = Novinky.objects.all().order_by('-datum_vytvoreni')
    return render(request, 'seznam_novinek.html', {
        'novinky': novinky,
        'form': form
    })


def detail_novinky(request, novinka_id):
    novinka = get_object_or_404(Novinky, pk=novinka_id)
    images = novinka.images.all()  # Získání všech obrázků
    form = None
    if request.user.is_authenticated:
        form = NovinkyForm(instance=novinka)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        if 'delete' in request.POST and request.user.has_perm('viewer.delete_novinky'):
            novinka.delete()
            return redirect('seznam_novinek')
        elif 'update' in request.POST and request.user.has_perm('viewer.change_novinky'):
            form = NovinkyForm(request.POST, request.FILES, instance=novinka)
            if form.is_valid():
                form.save()
                # Přidáno zpracování obrázků
                for image in request.FILES.getlist('images'):
                    NovinkyImage.objects.create(
                        novinka=novinka,
                        image=image
                    )
                return redirect('detail_novinky', novinka_id=novinka.id)

    return render(request, 'detail_novinky.html', {
        'novinka': novinka,
        'form': form if request.user.is_authenticated else None,
        'images': images  # Přidání obrázků do kontextu
    })


@login_required
@permission_required('viewer.add_novinky')
def pridat_novinku(request):
    if request.method == 'POST':
        form = NovinkyForm(request.POST, request.FILES)
        if form.is_valid():
            novinka = form.save(commit=False)
            novinka.autor = request.user
            novinka.save()

            # Zpracování více obrázků
            for image in request.FILES.getlist('images'):
                NovinkyImage.objects.create(
                    novinka=novinka,
                    image=image
                )
            return redirect('seznam_novinek')
    else:
        form = NovinkyForm()
    return render(request, 'pridat_novinku.html', {'form': form})


@login_required
@permission_required('viewer.delete_novinky')
def smazat_novinku(request, novinka_id):
    novinka = get_object_or_404(Novinky, pk=novinka_id)
    if request.method == 'POST':
        novinka.delete()
        return redirect('seznam_novinek')
    return render(request, 'smazat_novinku.html', {'novinka': novinka})


class BaseReviewEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    fields = ['rating', 'comment']
    template_name = 'review_form.html'

    def test_func(self):
        review = self.get_object()
        return (self.request.user.is_superuser or
                self.request.user == review.user or
                self.request.user.has_perm('viewer.change_review'))

    def form_valid(self, form):
        response = super().form_valid(form)
        if (self.request.user.is_superuser or
            self.request.user.has_perm('edit_review')) and \
                self.request.user != self.object.user:
            messages.warning(self.request, f'Upravili jste recenzi uživatele {self.object.user} jako administrátor.')
        else:
            messages.success(self.request, 'Recenze byla úspěšně upravena.')
        return response


class BaseReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = 'review_confirm_delete.html'

    def test_func(self):
        review = self.get_object()
        return (self.request.user.is_superuser or
                self.request.user == review.user or
                self.request.user.has_perm('viewer.delete_review'))

    def delete(self, request, *args, **kwargs):
        review = self.get_object()
        if (request.user.is_superuser or request.user.has_perm('viewer.delete_review')) and request.user != review.user:
            messages.warning(request, f'Smazali jste recenzi uživatele {review.user} jako administrátor.')
        else:
            messages.success(request, 'Recenze byla úspěšně smazána.')
        return super().delete(request, *args, **kwargs)


class PedikuraReviewCreateView(LoginRequiredMixin, CreateView):
    model = PedikuraReview
    form_class = PedikuraReviewForm
    template_name = 'review_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.pedikura_id = self.kwargs['pk']
        messages.success(self.request, 'Vaše hodnocení bylo úspěšně přidáno.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('pedicure_detail', kwargs={'pk': self.kwargs['pk']})


class PedikuraReviewEditView(BaseReviewEditView):
    model = PedikuraReview
    template_name = 'review_form.html'
    fields = ['rating', 'comment']

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        print(f"Editing review ID: {obj.id}, User: {obj.user}, Pedikura: {obj.pedikura.pk}")
        return obj

    def get_success_url(self):
        return reverse_lazy('pedicure_detail', kwargs={'pk': self.object.pedikura.pk})


class PedikuraReviewDeleteView(BaseReviewDeleteView):
    model = PedikuraReview
    template_name = 'confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('pedicure_detail', kwargs={'pk': self.object.pedikura.pk})


class RasyReviewCreateView(LoginRequiredMixin, CreateView):
    model = RasyReview
    form_class = RasyReviewForm
    template_name = 'review_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.rasy_id = self.kwargs['pk']
        messages.success(self.request, 'Vaše hodnocení bylo úspěšně přidáno.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('eyelash_detail', kwargs={'pk': self.kwargs['pk']})


class RasyReviewEditView(BaseReviewEditView):
    model = RasyReview
    template_name = 'review_form.html'

    def get_success_url(self):
        return reverse_lazy('eyelash_detail', kwargs={'pk': self.object.rasy.pk})


class RasyReviewDeleteView(BaseReviewDeleteView):
    model = RasyReview
    template_name = 'confirm_delete.html'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if not (request.user == obj.user or request.user.is_superuser or request.user.has_perm('viewer.delete_review')):
            messages.error(request, 'Nemáte oprávnění smazat tuto recenzi.')
            return redirect('eyelash_detail', pk=obj.eyelash.pk)
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Recenze byla úspěšně smazána.')
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('eyelash_detail', kwargs={'pk': self.object.eyelash.pk})


class ZdraviReviewCreateView(LoginRequiredMixin, CreateView):
    model = ZdraviReview
    form_class = ZdraviReviewForm
    template_name = 'review_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.zdravi_id = self.kwargs['pk']
        messages.success(self.request, 'Vaše hodnocení bylo úspěšně přidáno.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('health_detail', kwargs={'pk': self.kwargs['pk']})


class ZdraviReviewEditView(BaseReviewEditView):
    model = ZdraviReview
    template_name = 'review_form.html'

    def get_success_url(self):
        return reverse_lazy('health_detail', kwargs={'pk': self.object.zdravi.pk})


class ZdraviReviewDeleteView(BaseReviewDeleteView):
    model = ZdraviReview
    template_name = 'confirm_delete.html'

    def dispatch(self, request, *args, **kwargs):
        # Kontrola oprávnění
        obj = self.get_object()
        if not (request.user == obj.user or request.user.is_superuser or request.user.has_perm('viewer.delete_review')):
            messages.error(request, 'Nemáte oprávnění smazat tuto recenzi.')
            return redirect('health_detail', pk=obj.zdravi.pk)
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Recenze byla úspěšně smazána.')
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('health_detail', kwargs={'pk': self.object.zdravi.pk})


class ContactReviewCreateView(LoginRequiredMixin, CreateView):
    model = ContactReview
    form_class = ContactReviewForm
    template_name = 'review_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.contact_id = self.kwargs['pk']
        messages.success(self.request, 'Vaše hodnocení bylo úspěšně přidáno.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('contact_detail', kwargs={'pk': self.kwargs['pk']})


class ContactReviewEditView(BaseReviewEditView):
    model = ContactReview
    template_name = 'review_form.html'
    fields = ['rating', 'comment', 'name', 'email']

    def get_success_url(self):
        return reverse_lazy('contact_detail', kwargs={'pk': self.object.contact.pk})


class ContactReviewDeleteView(BaseReviewDeleteView):
    model = ContactReview
    template_name = 'confirm_delete.html'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if not (request.user == obj.user or request.user.is_superuser or request.user.has_perm('viewer.delete_review')):
            messages.error(request, 'Nemáte oprávnění smazat tuto recenzi.')
            return redirect('contact_detail', pk=obj.contact.pk)
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Recenze byla úspěšně smazána.')
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('contact_detail', kwargs={'pk': self.object.contact.pk})
