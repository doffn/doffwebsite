from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("api/health/", views.health, name="health"),
    path("api/projects/", views.projects_api, name="projects_api"),
    path("api/contact/", views.contact_api, name="contact_api"),
]
