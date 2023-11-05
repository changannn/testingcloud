from django.urls import path
from . import views

app_name = "recipes"
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("recipe/<int:recipe_id>", views.view_recipe, name="view_recipe"),
    path("myrecipes", views.my_recipes, name="my_recipes"),
    path("myrecipes/update/<int:recipe_id>", views.update_recipe, name="update_recipe"),
    path("myrecipes/delete/<int:recipe_id>", views.delete_recipe, name="delete_recipe"),
    path("search", views.search, name="search"),
    path("add_to_favourites/<int:recipe_id>", views.add_to_favourites, name="add_to_favourites"),
    path("myfavourites", views.my_favourites, name="my_favourites"),
    path('remove_from_favourites/<int:recipe_id>/', views.remove_from_favourites, name='remove_from_favourites'),
    path("popular", views.popular_recipes, name="popular_recipes"),
]