from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.db.models import Q
from django.shortcuts import render, redirect
from .models import Favourites, Recipes
from django.db.models import Count

from .models import User, Recipes, Favourites
from django.contrib import messages




@login_required
def create(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        cuisine = request.POST["cuisine"]
        time = request.POST["time"]
        ingredients = request.POST.getlist('ingredients[]')
        steps = request.POST.getlist('steps[]')
        calories = request.POST["calories"]
        image = request.POST['image']
        owner_id = request.user

        # Save the data to the Recipes model
        recipe = Recipes(
            title=title,
            description=description,
            cuisine=cuisine,
            time=time,
            ingredients=ingredients,
            steps=steps,
            calories=calories,
            image=image,
            owner=owner_id
        )
        recipe.save()

        return HttpResponseRedirect(reverse("recipes:index"))
    else:
        return render(request, "recipes/create.html")


@login_required
def my_recipes(request):
    user = request.user
    user_recipes = Recipes.objects.filter(owner=user)
    return render(request, "recipes/my_recipes.html", {
        "user_recipes": user_recipes
    })



@login_required
def update_recipe(request, recipe_id):
    # Ensure the recipe belongs to the logged-in user
    try:
        recipe = Recipes.objects.get(id=recipe_id, owner=request.user)
    except Recipes.DoesNotExist:
        return HttpResponse("Recipe not found or you don't have permission to update it.")

    if request.method == "POST":
        # Update the recipe based on the form data
        recipe.title = request.POST["title"]
        recipe.description = request.POST["description"]
        recipe.cuisine = request.POST["cuisine"]
        recipe.time = request.POST["time"]
        recipe.ingredients = request.POST.getlist("ingredients[]")
        recipe.steps = request.POST.getlist("steps[]")
        recipe.calories = request.POST["calories"]
        recipe.image = request.POST["image"]
        recipe.save()
        return HttpResponseRedirect(reverse("recipes:my_recipes"))

    return render(request, "recipes/update_recipe.html", {
        "recipe": recipe
    })


@login_required
def delete_recipe(request, recipe_id):
    # Ensure the recipe belongs to the logged-in user
    try:
        recipe = Recipes.objects.get(id=recipe_id, owner=request.user)
    except Recipes.DoesNotExist:
        return HttpResponse("Recipe not found or you don't have permission to delete it.")

    if request.method == "POST":
        # Delete the recipe
        recipe.delete()
        return HttpResponseRedirect(reverse("recipes:my_recipes"))

    return render(request, "recipes/delete_recipe.html", {
        "recipe": recipe
    })



