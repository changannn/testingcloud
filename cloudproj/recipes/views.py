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


# @login_required
def index(request):
    if request.user.is_authenticated:
        user_favorites = Favourites.objects.filter(owner=request.user)
        favorite_recipes = [fav.title for fav in user_favorites]
    else:
        favorite_recipes = []  # Initialize as an empty list if the user is not authenticated.

    return render(request, "recipes/index.html", {
        "recipes": Recipes.objects.all(),
        "favorite_recipes": favorite_recipes,
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("recipes:index"))
        else:
            return render(request, "recipes/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "recipes/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("recipes:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "recipes/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "recipes/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("recipes:index"))
    else:
        return render(request, "recipes/register.html")


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


def view_recipe(request, recipe_id):
    recipe = Recipes.objects.get(id=recipe_id)
    return render(request, "recipes/view_recipe.html", {
        "recipe": recipe
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


def search(request):
    if request.method == "POST":
        query = request.POST.get("q")
        sort_by_calories = request.GET.get("sort_by_calories")
        query_without_spaces = query.strip()
        if query_without_spaces:
            # Create Q objects for each searchable field
            title_condition = Q(title__icontains=query)
            description_condition = Q(description__icontains=query)
            cuisine_condition = Q(cuisine__icontains=query)

            # Combine the conditions using the | (OR) operator
            conditions = title_condition | description_condition | cuisine_condition

            # Filter recipes that match the search conditions
            results = Recipes.objects.filter(conditions)

            results = results.exclude(~title_condition & ~description_condition & ~cuisine_condition)
            search_performed = True

            results = results.order_by('-likes')

            return render(request, "recipes/index.html", {
                "recipes": results,
                "search_performed": search_performed,
            })
        else:
            # Handle GET requests
            return HttpResponseRedirect(reverse("recipes:index"))

@login_required
def add_to_favourites(request, recipe_id):
    user = request.user
    recipe = get_object_or_404(Recipes, pk=recipe_id)

    # Check if the recipe is already in favorites
    if Favourites.objects.filter(owner=user, title=recipe).exists():
        messages.error(request, "Recipe is already in your favorites.")
    else:
        # Add the recipe to favorites
        Favourites.objects.create(owner=user, title=recipe)

        # Increment the likes count for the recipe
        recipe.likes += 1
        recipe.save()

        messages.success(request, "Recipe added to favorites successfully.")

    return redirect('recipes:index')  # Redirect to your index page

@login_required
def remove_from_favourites(request, recipe_id):
    user = request.user
    recipe = get_object_or_404(Recipes, pk=recipe_id)

    try:
        favorite = Favourites.objects.get(owner=user, title=recipe)
        favorite.delete()

        # Decrement the likes count for the recipe
        if recipe.likes > 0:
            recipe.likes -= 1
            recipe.save()

        messages.success(request, "Recipe removed from favorites successfully.")
    except Favourites.DoesNotExist:
        messages.error(request, "Recipe is not in your favorites.")

    return redirect('recipes:index')  # Redirect to your index page


def my_favourites(request):
    if request.user.is_authenticated:
        user = request.user
        user_favorites = Favourites.objects.filter(owner=user)
        favorite_recipes = [fav.title for fav in user_favorites]
        print(favorite_recipes)
        return render(request, "recipes/my_favourites.html", {"favorite_recipes": favorite_recipes})
    else:
        return redirect("recipes:index")


def popular_recipes(request):
    popular_recipes = (
        Recipes.objects.all().order_by('-likes')
    )

    return render(request, "recipes/popular_recipes.html", {"popular_recipes": popular_recipes})