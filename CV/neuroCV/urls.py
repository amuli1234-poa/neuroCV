from django.urls import path
from . import views

urlpatterns = [
    path('', views.neuroCV, name='neuroCV'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    
   path('resume/<int:pk>/', views.resume, name='resume'),
    
    path('edit/<int:cv_id>/', views.edit_cv, name='edit_cv'),
    path('delete/<int:cv_id>/', views.delete_cv, name='delete_cv'),
]