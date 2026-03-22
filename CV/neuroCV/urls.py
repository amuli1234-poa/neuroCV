from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.neuroCV, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('resume/<int:pk>/', views.resume_detail, name='resume_detail'), # Your current resume view
    path('resume/<int:pk>/edit/', views.edit_resume, name='edit_resume'),
    path('resume/<int:pk>/delete/', views.delete_resume, name='delete_resume'),
    



    # ... your existing urls ...
    
    # Login / Logout
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Change Password
    path('password-change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),
    path('pay/<int:pk>/', views.initiate_payment, name='initiate_payment'),
path('mpesa-callback/<int:resume_id>/', views.mpesa_callback, name='mpesa_callback'),
]
