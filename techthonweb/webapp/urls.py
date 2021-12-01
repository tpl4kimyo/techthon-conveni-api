from django.urls import path
from webapp import views

urlpatterns = [
    path('check', views.check_api),
]
