from django.urls import path

from .views import OrderCreateView, OrderListView, order_detail

app_name = 'orders'

urlpatterns = [
    path('create/', OrderCreateView.as_view(), name='create'),
    path('<int:pk>', order_detail, name='detail'),
    path('', OrderListView.as_view(), name='list'),
 ]