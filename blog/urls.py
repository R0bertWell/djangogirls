from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('posts/<int:author>', views.post_list, name='post_list_by_author'),
    path('post/<int:pk>', views.post_detail, name='post_detail'),
    path('post/new', views.post_new, name='post_new'),
    path('post/edit/<int:pk>', views.post_edit, name='post_edit'),
]