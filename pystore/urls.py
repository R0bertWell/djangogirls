from django.urls import path
from .views import ProductListView, ProductDetailView, LoginView, LogoutView, SignupView


app_name = 'pystore'

urlpatterns = [
    path('', ProductListView.as_view(), name='list'),
    path('category/<slug:slug>', ProductListView.as_view(), name='list_by_category'),
    path('<slug:slug>', ProductDetailView.as_view(), name='detail'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
]