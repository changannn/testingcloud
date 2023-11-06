from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core import serializers
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.db.models import Q
from django.shortcuts import render, redirect
from .models import Favourites, Recipes
from django.db.models import Count

from .models import User, Recipes, Favourites
from django.contrib import messages
import json
import requests
import logging

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


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


def view_recipe(request, recipe_id):
    recipe = Recipes.objects.get(id=recipe_id)
    return render(request, "recipes/view_recipe.html", {
        "recipe": recipe
    })

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

@csrf_exempt
def display_search(request):
    if request.method == 'POST':
        search_query = request.POST.get('q', '')
        # Make a POST request to the search-microservice
        response = requests.post('http://search-microservice:8002/search', data={'q': search_query})
        if response.status_code == 200:
            # Deserialize the JSON string into Python objects
            search_results_json = json.loads(response.json()['results'])
            # Transform the search results to the format expected by the template
            recipes = [
                {
                    'id': result['pk'],
                    'title': result['fields']['title'],
                    'description': result['fields']['description'],
                    'cuisine': result['fields']['cuisine'],
                    'time': result['fields']['time'],
                    'calories': result['fields']['calories'],
                    'image': result['fields']['image'],
                    'likes': result['fields']['likes']
                } for result in search_results_json
            ]
            
            # Now you can pass these transformed objects to your template
            return render(request, "recipes/index.html", {
                "recipes": recipes,
                "search_performed": True,
            })
        else:
            # Handle errors
            return JsonResponse({'error': 'Search service is currently unavailable.'}, status=503)
    else:
        # Return an empty form or a default page if not a POST request
        return render(request, "recipes/index.html")
