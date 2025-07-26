from django.urls import path
from . import views

urlpatterns = [
    path('', views.ads_list, name='ads_list'),
    path('new/', views.create_ad, name='create_ad'),
    path('<int:pk>/edit/', views.edit_ad, name='edit_ad'),
]
