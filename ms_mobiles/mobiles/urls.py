from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('mobiles/', views.mobiles, name='mobiles'),
    path('mobiles/<int:id>/', views.mobile_detail, name='mobile_detail'),

    path('repair/', views.repair, name='repair'),
    path('track-repair/', views.track_repair, name='track_repair'),

    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('cart/', views.cart, name='cart'),
    path('place-order/<int:id>/', views.place_order, name='place_order'),

    path('robots.txt', views.robots_txt, name='robots_txt'),
]