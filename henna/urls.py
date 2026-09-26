from django.urls import path
from . import views

app_name = "henna"

urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('gallery/', views.gallery, name="gallery"),
    path('products/', views.products, name="products"),
]