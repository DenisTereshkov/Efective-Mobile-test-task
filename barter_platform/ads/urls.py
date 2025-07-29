from django.urls import path
from . import views

urlpatterns = [
    path('', views.ads_list, name='ads_list'),
    path('new/', views.create_ad, name='create'),
    path('profile/', views.user_profile, name='profile'),
    path('<int:pk>/create-exchange/', views.create_exchange, name='create_exchange'),
    path('<int:pk>/', views.ad_detail, name='detail'),
    path('<int:pk>/edit/', views.edit_ad, name='edit'),
    path('<int:pk>/delete/', views.delete_ad, name='delete'),
    path('my-exchanges/', views.incoming_exchanges, name='exchange_to_me'),
    path('accept-exchange/<int:exchange_id>/', views.accept_exchange, name='accept_exchange'),
    path('reject-exchange/<int:exchange_id>/', views.reject_exchange, name='reject_exchange'),
    path('reject-exchange/<int:exchange_id>/', views.cancel_exchange, name='cancel_exchange'),
]
