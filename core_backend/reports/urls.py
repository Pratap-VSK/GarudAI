from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('api/submit/', views.submit_incident, name='submit_incident'),
]