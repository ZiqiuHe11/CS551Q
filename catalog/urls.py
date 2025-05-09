from django.urls import path
from . import views

urlpatterns = [
    path('', views.star_list, name='star_list'),
    path('star/<int:pk>/', views.star_detail, name='star_detail'),
    path('order/', views.create_order, name='create_order'),
    path('orders/', views.my_orders, name='my_orders'),
    path('orders/<int:pk>/pay/', views.pay_for_order, name='pay_for_order'),
    path('orders/<int:pk>/confirm/', views.confirm_order, name='confirm_order'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin-orders/', views.admin_orders, name='admin_orders'),
    path('register/', views.register, name='register'),
]

