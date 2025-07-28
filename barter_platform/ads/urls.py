from django.urls import path
from . import views

urlpatterns = [
    path('', views.ads_list, name='ads_list'),
    path('new/', views.create_ad, name='create'),
    path('profile/', views.user_profile, name='profile'),
    path('<int:pk>/', views.ad_detail, name='detail'),
    path('<int:pk>/edit/', views.edit_ad, name='edit'),
    path('<int:pk>/delete/', views.delete_ad, name='delete'),
]
