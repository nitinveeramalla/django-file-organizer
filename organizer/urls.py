from django.urls import path
from . import views

app_name = 'organizer'

urlpatterns = [
    path('', views.home, name='home'),
    path('results/<str:session_id>/', views.results, name='results'),
    path('analytics/', views.analytics, name='analytics'),
]
