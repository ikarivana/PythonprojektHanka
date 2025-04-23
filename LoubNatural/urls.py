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

from viewer.views import *

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', Home, name="home"),
    path('pedicure/', PedicureListView.as_view(), name="pedicure"),
    path('pedicure/<int:pk>/', PedicureDetailView.as_view(), name="pedicure_detail"),
    path('pedikure/', PedicureCreateView.as_view(), name="pedicure_create"),
    path('pedicure/update/<int:pk>/', PedicureUpdateView.as_view(), name="pedicure_update"),
    path('pedicure/delete/<int:pk>/', PedicureDeleteView.as_view(), name="pedicure_delete"),

    path('eyelash/', EyelashListView.as_view(), name="eyelash"),
    path('eyelash/<int:pk>/', EyelashDetailView.as_view(), name="eyelash_detail"),
    path('eyelash/', EyelashCreateView.as_view(), name="eyelash_create"),
    path('eyelash/update/<int:pk>/', EyelashUpdateView.as_view(), name="eyelash_update"),
    path('eyelash/delete/<int:pk>/', EyelashDeleteView.as_view(), name="eyelash_delete"),

]
