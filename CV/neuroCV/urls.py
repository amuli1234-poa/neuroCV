from django.urls import path
from . import views

urlpatterns = [
    path('', views.neuroCV, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('resume/<int:pk>/', views.resume_detail, name='resume_detail'), # Your current resume view
    path('resume/<int:pk>/edit/', views.edit_resume, name='edit_resume'),
    path('resume/<int:pk>/delete/', views.delete_resume, name='delete_resume'),
]