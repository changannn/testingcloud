from django.urls import path
from . import views

app_name = "recipes"
urlpatterns = [
    path("", views.index, name="index"),
    path("recipe/<int:recipe_id>", views.view_recipe, name="view_recipe"),
    path("add_to_favourites/<int:recipe_id>", views.add_to_favourites, name="add_to_favourites"),
    path("myfavourites", views.my_favourites, name="my_favourites"),
    path('remove_from_favourites/<int:recipe_id>/', views.remove_from_favourites, name='remove_from_favourites'),
    path("popular", views.popular_recipes, name="popular_recipes"),
    path("search", views.display_search, name="display_search"),
]