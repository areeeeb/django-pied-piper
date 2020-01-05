from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('text_compress/', views.text_compress_view, name='text-compress'),
    path('text_decompress/', views.text_decompress_view, name='text-decompress'),
    path('image_compress/', views.image_compress_view, name='image-compress'),
    path('image_decompress/', views.image_decompress_view, name='image-decompress'),
    path('compressed-file_download/<file_name>/',
         views.download_compressed_file_view,
         name='download-compressed-file'),
    path('text-file_download/<file_name>/',
         views.download_text_file_view,
         name='download-text-file'),
    path('image-file_download/<file_name>/',
         views.download_image_file_view,
         name='download-image-file'),
]
