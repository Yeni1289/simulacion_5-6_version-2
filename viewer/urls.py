from django.urls import path
from . import views

urlpatterns = [
    path('', views.loader_view, name='loader'),
    path('browse/', views.browse_notebooks, name='browse'),
    path('api/scan-folder/', views.scan_folder, name='scan_folder'),
    path('api/process-notebook/', views.process_notebook, name='process_notebook'),
    path('notebook/<str:slug>/', views.notebook_detail, name='notebook_detail'),
]
