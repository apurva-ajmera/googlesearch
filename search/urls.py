from django.urls import path
from . import views

urlpatterns = [
    path('search-console/register', views.register, name='register'),
]
