from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('report/', views.index, name='report'),  
    path('api/submit/', views.submit_incident, name='api_submit'),
    path('my-reports/', views.my_reports, name='my_reports'),
    path('api/submit/', views.submit_incident, name='api_submit'),
    path('api/submit/', views.submit_incident, name='api_submit'),
    path('api/confirm/', views.confirm_incident, name='api_confirm'),
]