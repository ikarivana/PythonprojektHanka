"""
URL configuration for LoubNatural project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path, include

from LoubNatural import settings
from accounts.views import (
    user_logout,
    SignUpView,
)
from viewer import views
from viewer.views import (
    search_view, name_day,
    PedicureListView, PedicureDetailView, PedicureCreateView, PedicureUpdateView, PedicureDeleteView,
    EyelashListView, EyelashDetailView, EyelashCreateView, EyelashUpdateView, EyelashDeleteView,
    HealthListView, HealthDetailView, HealthCreateView, HealthUpdateView, HealthDeleteView,
    ContactListView, ContactDetailView, ContactCreateView, ContactUpdateView, ContactDeleteView,
    ImageCreateView, ImageListView, ImageDetailView, ImageUpdateView, ImageDeleteView,
    OrderListView, OrderCreateView,
)

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('search/', search_view, name='search'),
                  path('', views.home, name='home'),



                  # Pedikúra
                  path('pedicure/', PedicureListView.as_view(), name='pedicure'),
                  path('pedicure/<int:pk>/', PedicureDetailView.as_view(), name='pedicure_detail'),
                  path('pedicure/create/', PedicureCreateView.as_view(), name='pedicure_create'),
                  path('pedicure/<int:pk>/update/', PedicureUpdateView.as_view(), name='pedicure_update'),
                  path('pedicure/<int:pk>/delete/', PedicureDeleteView.as_view(), name='pedicure_delete'),
                  path('pedicure/<int:pk>/review/', views.PedikuraReviewCreateView.as_view(), name='pedicure_review'),
                  path('pedicure/review/<int:pk>/edit/', views.PedikuraReviewEditView.as_view(),
                       name='pedicure_review_edit'),
                  path('pedicure/review/<int:pk>/delete/', views.PedikuraReviewDeleteView.as_view(),
                       name='pedicure_review_delete'),

                  # Řasy
                  path('eyelash/', EyelashListView.as_view(), name='eyelash'),
                  path('eyelash/<int:pk>/', EyelashDetailView.as_view(), name='eyelash_detail'),
                  path('eyelash/create/', EyelashCreateView.as_view(), name='eyelash_create'),
                  path('eyelash/<int:pk>/update/', EyelashUpdateView.as_view(), name='eyelash_update'),
                  path('eyelash/<int:pk>/delete/', EyelashDeleteView.as_view(), name='eyelash_delete'),
                  path('eyelash/<int:pk>/review/', views.RasyReviewCreateView.as_view(), name='eyelash_review'),
                  path('eyelash/review/<int:pk>/edit/', views.RasyReviewEditView.as_view(), name='eyelash_review_edit'),
                  path('eyelash/review/<int:pk>/delete/', views.RasyReviewDeleteView.as_view(),
                       name='eyelash_review_delete'),

                  # Zdraví
                  path('health/', HealthListView.as_view(), name='health'),
                  path('health/<int:pk>/', HealthDetailView.as_view(), name='health_detail'),
                  path('health/create/', HealthCreateView.as_view(), name='health_create'),
                  path('health/<int:pk>/update/', HealthUpdateView.as_view(), name='health_update'),
                  path('health/<int:pk>/delete/', HealthDeleteView.as_view(), name='health_delete'),
                  path('health/<int:pk>/review/', views.ZdraviReviewCreateView.as_view(), name='health_review'),
                  path('health/review/<int:pk>/edit/', views.ZdraviReviewEditView.as_view(), name='health_review_edit'),
                  path('health/review/<int:pk>/delete/', views.ZdraviReviewDeleteView.as_view(),
                       name='health_review_delete'),

                  # Kontakt
                  path('contact/', ContactListView.as_view(), name='contact'),
                  path('contact/<int:pk>/', ContactDetailView.as_view(), name='contact_detail'),
                  path('contact/create/', ContactCreateView.as_view(), name='contact_create'),
                  path('contact/<int:pk>/update/', ContactUpdateView.as_view(), name='contact_update'),
                  path('contact/<int:pk>/delete/', ContactDeleteView.as_view(), name='contact_delete'),
                  path('contact/<int:pk>/review/', views.ContactReviewCreateView.as_view(), name='contact_review'),
                  path('contact/review/<int:pk>/edit/', views.ContactReviewEditView.as_view(),
                       name='contact_review_edit'),
                  path('contact/review/<int:pk>/delete/', views.ContactReviewDeleteView.as_view(),
                       name='contact_review_delete'),

                  path('objednavky/', OrderListView.as_view(), name='order_list'),
                  path('objednavky/vytvorit/', OrderCreateView.as_view(), name='order_create'),

                  path('login/', LoginView.as_view(), name='login'),
                  path('accounts/logout/', user_logout, name="logout"),
                  path('accounts/', include('django.contrib.auth.urls')),
                  path('accounts/signup/', SignUpView.as_view(), name="signup"),


                  path('images/', ImageListView.as_view(), name='images'),
                  path('image/<int:pk>/', ImageDetailView.as_view(), name='image'),
                  path('image/create/', ImageCreateView.as_view(), name='image_create'),
                  path('image/update/<int:pk>/', ImageUpdateView.as_view(), name='image_update'),
                  path('image/delete/<int:pk>/', ImageDeleteView.as_view(), name='image_delete'),

                  path('nameday/', name_day, name='nameday'),

                  path('novinky/', views.seznam_novinek, name='seznam_novinek'),
                  path('novinky/<int:novinka_id>/', views.detail_novinky, name='detail_novinky'),
                  path('novinky/pridat/', views.pridat_novinku, name='pridat_novinku'),
                  path('novinky/smazat/<int:novinka_id>/', views.smazat_novinku, name='smazat_novinku'),

                  path('', include(('viewer.urls', 'viewer'), namespace='viewer')),


              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
