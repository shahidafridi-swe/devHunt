
from django.urls import path
from . import models 

urlpatterns = [
    path("projects/", models.projects, name="projects"),
]
