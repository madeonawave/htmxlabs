"""
other_views.py

Contains Django views for utility endpoints, APIs, or views not fitting in main or examples.
"""

from django.shortcuts import render

def htmx_rest_api_demo(request):
    return render(request, "demo/htmx-rest-api.html", )

# Add other utility/API views here as needed.