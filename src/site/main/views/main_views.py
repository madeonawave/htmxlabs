"""
main_views.py

Contains Django views for main site pages (homepage, docs, about, contact, etc.).
"""

import random
import datetime
from django.shortcuts import render
from django.http import HttpResponse, Http404, FileResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return render(request, 'index.html')

quotes = [
    "Full-stack with half the stack",
    "Less is more, HTML is most",
    "Simplicity scales",
    "Zero dependencies, infinite possibilities",
    "The anti-framework framework",
    "One library to unbundle them all",
    "Less JavaScript, more joy",
    "Why build when you can just... not?"
]

def carousel(request, id):
    # Select content based on id
    context = {"id": id}
    if id == "quickstart":
        context.update({
            "title": "HTMX",
            "description": random.choice(quotes),
            "button_text": "Try HTMX",
            "result_id": "carousel-quickstart-result",
            "tags": ["Beginner", "Quick Start"],
            "example": "quickstart"
        })
    elif id == "like":
        context.update({
            "title": "Partial Page Updates",
            "description": "HTMX can update parts of a page without a full-page request.",
            "button_text": "Show HTMX Example",
            "result_id": "htmx-code-demo",
            "tags": ["UI", "Beginner"],
            "example": "like"
        })
    elif id == "live-search":
        context.update({
            "title": "Example: Live Search",
            "description": "Updates live suggestions from the backend, using HTMX.",
            "button_text": "Search",
            "result_id": "carousel-search-result",
            "tags": ["Search", "AJAX"],
            "example": "live-search"
        })
    elif id == "polling":
        context.update({
            "title": "Example: Live Stock Ticker",
            "description": "See real-time Bitcoin price updates using HTMX polling.",
            "button_text": "Show Ticker",
            "result_id": "carousel-ticker-result",
            "tags": ["Real-time", "Polling", "API"],
            "example": "ticker"
        })
    else:
        context.update({
            "title": "Unknown Example",
            "description": "No example found for this id.",
            "button_text": "",
            "result_id": "",
            "tags": [],
            "example": "none"
        })
    return render(request, 'carousel.html', context)

def documentation(request):
    """
    Renders the main documentation landing page.
    """
    return render(request, "docs/index.html")

def docs_getting_started(request):
    """
    Renders the Getting Started documentation page.
    """
    return render(request, "docs/getting-started.html")

def docs_core_attributes(request):
    """
    Renders the Core Attributes documentation page.
    """
    return render(request, "docs/core-attributes.html")

def favicon(request):
    """
    Serve the favicon.svg file. If not found, return an empty SVG.
    """
    import os
    favicon_path = os.path.join(settings.BASE_DIR, "static", "main", "favicon.svg")
    try:
        return FileResponse(open(favicon_path, "rb"), content_type="image/svg+xml")
    except Exception:
        empty_svg = '<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32"></svg>'
        return HttpResponse(empty_svg, content_type="image/svg+xml")





def reference_api(request):
    return render(request, "frontend/api_reference.html", )

def about_modal(request):
    return render(request, "about_modal.html")

def careers_modal(request):
    return render(request, "careers_modal.html")

@csrf_exempt
def contact(request):
    if request.method != "POST":
        # If HTMX, return modal fragment, else render page (for direct navigation)
        if request.headers.get("HX-Request"):
            return render(request, "contact_form_fragment.html")
        else:
            return render(request, "contact.html")
    name = request.POST.get("name", "").strip()
    email = request.POST.get("email", "").strip()
    message = request.POST.get("message", "").strip()
    errors = []
    if not name:
        errors.append("Name is required.")
    if not email:
        errors.append("Email is required.")
    if not message:
        errors.append("Message is required.")
    if errors:
        return render(request, "contact_form_fragment.html", {
            "errors": errors,
            "name": name,
            "email": email,
            "message": message,
        })
    ContactMessage.objects.create(name=name, email=email, message=message)
    return render(request, "contact_success_fragment.html", {"name": name})