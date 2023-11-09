from django.urls import path
from . import views

app_name = "recipes"
urlpatterns = [
    path("create", views.create, name="create"),
    path("myrecipes", views.my_recipes, name="my_recipes"),
    path("myrecipes/update/<int:recipe_id>", views.update_recipe, name="update_recipe"),
    path("myrecipes/delete/<int:recipe_id>", views.delete_recipe, name="delete_recipe"),
    path("recipe/<int:recipe_id>", views.view_recipe, name="view_recipe"),
]