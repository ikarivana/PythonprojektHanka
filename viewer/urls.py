from django.urls import path

from .views import OrderListView, OrderCreateView

app_name = 'viewer'

urlpatterns = [
    path('objednavky/', OrderListView.as_view(), name='order-list'),
    path('nova/', OrderCreateView.as_view(), name='order-create'),


]


