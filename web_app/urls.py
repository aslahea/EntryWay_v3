from django.urls import path
from . import views
from django.shortcuts import redirect

urlpatterns = [

    # 👤 User Routes
    path('', views.welcome_view, name='welcome'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('home/', views.home_view, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('update-bio/', views.update_bio, name='update_bio'),
    path('soft-delete-user/<int:user_id>/',
         views.soft_delete_user, name='soft_delete_user'),

    # 🛠 Admin Panel Routes
    path('administrator/admin-login/',
         views.admin_login_view, name='admin_login'),
    path('administrator/admin-dash/',
         views.admin_dashboard, name='admin_dashboard'),
    path('administrator/admin-logout/',
         views.admin_logout_view, name='admin_logout'),
    path('administrator/edit-user/<int:user_id>/',
         views.admin_edit_user, name='admin_edit_user'),
    path('administrator/delete-user/<int:user_id>/',
         views.admin_soft_delete_user, name='admin_soft_delete_user'),
    path('administrator/add-user/',
         views.admin_create_user, name='admin_create_user'),



]
