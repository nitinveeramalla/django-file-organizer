from django.urls import path
from . import views

app_name = 'organizer'

urlpatterns = [
    path('', views.home, name='home'),
    path('results/<str:session_id>/', views.results, name='results'),
    path('analytics/', views.analytics, name='analytics'),
    path('download-csv/', views.download_csv, name='download_csv'),
    path('download-csv/<str:session_id>/', views.download_csv, name='download_csv_session'),
]
