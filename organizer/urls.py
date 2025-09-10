from django.urls import path
from . import views

app_name = 'organizer'

urlpatterns = [
    path('', views.index, name='index'),
    path('results/', views.results, name='results'),
    path('analytics/', views.analytics, name='analytics'),
    path('api/analytics/', views.analytics_api, name='analytics_api'),
    path('session/<str:session_id>/', views.session_detail, name='session_detail'),
]
