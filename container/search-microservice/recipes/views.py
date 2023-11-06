from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.db.models import Q
from django.shortcuts import render, redirect
from .models import Favourites, Recipes
from django.db.models import Count

from .models import User, Recipes, Favourites
from django.contrib import messages

import requests
import logging

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


@csrf_exempt
def search(request):
    if request.method == "POST":
        query = request.POST.get("q", "")
        logger.debug(f"Search query received: {query}")

        query_without_spaces = query.strip()
        if query_without_spaces:
            logger.debug("Processing the search query.")
            title_condition = Q(title__icontains=query)
            description_condition = Q(description__icontains=query)
            cuisine_condition = Q(cuisine__icontains=query)

            conditions = title_condition | description_condition | cuisine_condition

            results = Recipes.objects.filter(conditions)
            logger.debug(f"Number of results found: {results.count()}")

            results = results.exclude(~title_condition & ~description_condition & ~cuisine_condition)
            results = results.order_by('-likes')

            # Serialize the results to JSON format
            results_json = serializers.serialize('json', results)
            logger.debug(f"Serialized search results: {results_json[:500]}")

            # Instead of sending the results to another microservice,
            # return them as a JsonResponse which will be the response to the AJAX request.
            return JsonResponse({'results': results_json})

        else:
            logger.warning("Search query is empty after stripping spaces.")
            return JsonResponse({'error': 'Empty search query'}, status=400)

    else:
        logger.warning("Search view accessed with non-POST request.")
        return JsonResponse({'error': 'Invalid request method'}, status=405)