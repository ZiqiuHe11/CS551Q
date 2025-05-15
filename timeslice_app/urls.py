from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),  
    path('search/', views.search_timeslices, name='search_timeslices'),
    path('buy/<int:timeslice_id>/', views.add_to_order, name='add_to_order'),
    path('order/success/<int:order_id>/', views.order_success, name='order_success'),
    path('category/', views.category_filter, name='category_filter'),
    path('location/', views.location_filter, name='location_filter'),
    path('detail/<int:timeslice_id>/', views.timeslice_detail, name='timeslice_detail'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('filter/', views.combined_filter, name='combined_filter'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', views.register, name='register'),  
    path('profile/', views.user_profile, name='user_profile'),

]

handler404 = 'timeslice_app.views.custom_404'
handler500 = 'timeslice_app.views.custom_500'
handler403 = 'timeslice_app.views.custom_403'
