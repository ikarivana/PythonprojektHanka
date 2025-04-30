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
from django.contrib import admin
from django.urls import path
from viewer.views import home, search, PedicureListView, PedicureDetailView, PedicureCreateView, PedicureUpdateView, PedicureDeleteView, EyelashListView, EyelashDetailView, EyelashCreateView, EyelashUpdateView, EyelashDeleteView, HealthListView, HealthDetailView, HealthCreateView, HealthUpdateView, HealthDeleteView, ContactListView, ContactDetailView, ContactCreateView, ContactUpdateView, ContactDeleteView



urlpatterns = [
    path('admin/', admin.site.urls),

    path('', home, name="home"),
    path('search/', search, name="search"),
    path('pedicure/', PedicureListView.as_view(), name="pedicure"),
    path('pedicure/<int:pk>/', PedicureDetailView.as_view(), name="pedicure_detail"),
    path('pedicure/create', PedicureCreateView.as_view(), name="pedicure_create"),
    path('pedicure/update/<int:pk>/', PedicureUpdateView.as_view(), name="pedicure_update"),
    path('pedicure/delete/<int:pk>/', PedicureDeleteView.as_view(), name="pedicure_delete"),

    path('eyelash/', EyelashListView.as_view(), name="eyelash"),
    path('eyelash/<int:pk>/', EyelashDetailView.as_view(), name="eyelash_detail"),
    path('eyelash/create', EyelashCreateView.as_view(), name="eyelash_create"),
    path('eyelash/update/<int:pk>/', EyelashUpdateView.as_view(), name="eyelash_update"),
    path('eyelash/delete/<int:pk>/', EyelashDeleteView.as_view(), name="eyelash_delete"),

    path('health/', HealthListView.as_view(), name="health"),
    path('health/<int:pk>/', HealthDetailView.as_view(), name="health_detail"),
    path('health/create', HealthCreateView.as_view(), name="health_create"),
    path('health/update/<int:pk>/', HealthUpdateView.as_view(), name="health_update"),
    path('health/delete/<int:pk>/', HealthDeleteView.as_view(), name="health_delete"),

    path('contact/', ContactListView.as_view(), name="contact"),
    path('contact/<int:pk>/', ContactDetailView.as_view(), name="contact_detail"),
    path('contact/create', ContactCreateView.as_view(), name="contact_create"),
    path('contact/update/<int:pk>/', ContactUpdateView.as_view(), name="contact_update"),
    path('contact/delete/<int:pk>/', ContactDeleteView.as_view(), name="contact_delete"),
]

