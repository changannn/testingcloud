from django.urls import path
from . import views

app_name = "recipes"
urlpatterns = [

    path("search", views.search, name="search"),
]