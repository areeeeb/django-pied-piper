from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('text_compress/', views.text_compress_view, name='text-compress'),
    path('image_compress/', views.image_compress_view, name='image-compress'),
]
