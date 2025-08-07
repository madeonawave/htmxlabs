import csv
import json
import os
import calendar
import datetime
import random
from io import StringIO
import markdown as md

import requests
from django.http import Http404, JsonResponse, HttpResponse, FileResponse
from django.shortcuts import render
from django.template import TemplateDoesNotExist
from django.views.decorators.csrf import csrf_exempt

from .utils import htmx_template

from django.views.decorators.csrf import csrf_exempt

from config import settings


def htmx_rest_api_demo(request):
    return render(request, "demo/htmx-rest-api.html", )

# --- Like Button Example State (in-memory for demo) ---
LIKE_BUTTON_STATE = {"count": 42, "liked": False}

@csrf_exempt
def like_button(request):
    """
    Handles the like button AJAX POST and returns the updated button fragment.
    """
    global LIKE_BUTTON_STATE
    if request.method == "POST":
        # Optimistic update: toggle liked state and update count
        if LIKE_BUTTON_STATE["liked"]:
            LIKE_BUTTON_STATE["count"] -= 1
            LIKE_BUTTON_STATE["liked"] = False
        else:
            LIKE_BUTTON_STATE["count"] += 1
            LIKE_BUTTON_STATE["liked"] = True
    # For GET or after POST, render the button
    return render(request, "demo/like-button.html", {
        "count": LIKE_BUTTON_STATE["count"],
        "liked": LIKE_BUTTON_STATE["liked"],
    })


def index(request):
    return render(request, 'index.html')

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


def examples(request):
    # Load examples from JSON
    import json
    with open('main/examples.json', 'r') as file:
        examples = json.load(file)
    return render(request, "full_examples.html", {"examples": examples})


def examples_data(request, filter_name):

    # Get filtered, sorted, paginated data
    q = request.GET.get('q', '').strip().lower()
    category = filter_name
    sort = request.GET.get('sort', 'popular')
    try:
        limit = int(request.GET.get('limit', 12))
    except ValueError:
        limit = 12
    try:
        offset = int(request.GET.get('offset', 0))
    except ValueError:
        offset = 0

    with open('main/examples.json', 'r') as file:
        data = json.load(file)

    # Filtering by category/tag/level
    if category and category != "all" and category != "search":
        data = [
            ex for ex in data
            if category in [t.lower() for t in ex.get("tags", [])]
               or ex.get("level", "").lower() == category
        ]

    # Filtering by search query
    if q and q != "":
        with open('main/examples.json', 'r') as file:
            data = json.load(file)

        data = [
            ex for ex in data
            if q in ex.get("title", "").lower()
               or q in ex.get("description", "").lower()
               or any(q in tag.lower() for tag in ex.get("tags", []))
        ]

    # Sorting
    if sort == "alphabetical":
        data = sorted(data, key=lambda x: x.get("title", ""))
    elif sort == "difficulty":
        order = {"beginner": 1, "intermediate": 2, "advanced": 3}
        data = sorted(data, key=lambda x: order.get(x.get("level", "").lower(), 99))
    elif sort == "newest":
        data = sorted(data, key=lambda x: x.get("timestamp", ""), reverse=True)
    # else: "popular" or default order, do nothing

    # Pagination
    total = len(data)
    paged = data[offset:offset + limit]
    # Render the grid partial template with the paged examples
    return render(request, "examples_grid.html",
                  {"examples": paged,
                   "total": total,
                   "offset": offset,
                   "limit": limit,
                   "loadmore": offset + limit < total})


def dynamic_page(request, page_name):
    # Whitelist allowed templates
    allowed_templates = [
        'active-search.html',
        'basic-ajax.html',
        'basic-ajax-response.html',
        'click-to-edit.html',
        'calendar.html',
        'clickme_example.html',
        'csv-export.html',
        'color-picker.html',
        'data-table.html',
        'delete-row.html',
        'drag-drop.html',
        'file-upload.html',
        'form-validation.html',
        'htmx_rest_api_demo.html',
        'infinite-scroll.html',
        'kanban-board.html',
        'lazy-load.html',
        'like-button.html',
        'live-search.html',
        'live-stock-ticker.html',
        'live-chat.html',
        'markdown-preview.html',
        'master-detail.html',
        'modal-dialog.html',
        'dependent-dropdowns.html',
        'tabbed-interface.html',
        'theme-switcher.html',
        'toast-notification.html',
        'sort-table.html',
        'progress-bar.html',
        'polling.html',
        'realtime-notifications.html',
        'weather-widget.html'
    ]
    templates_folder = 'demo'

    if f'{page_name}' not in allowed_templates:
        raise Http404("Page not found")
    template_name = f'{templates_folder}/{page_name}'
    try:
        return render(request, template_name)
    except TemplateDoesNotExist as e:
        raise Http404("Page not found") from e


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

@csrf_exempt
def click_to_edit_form(request):
    """
    Returns the inline edit form for Click to Edit example.
    """
    value = request.GET.get("value", "This is editable text. Click to edit.")
    return render(request, "demo/click-to-edit-form.html", {"value": value})

@csrf_exempt
def click_to_edit_save(request):
    """
    Handles saving the edited value and returns the display span.
    """
    value = request.POST.get("value", "This is editable text. Click to edit.")
    return render(request, "demo/click-to-edit-save.html", {"value": value})

@csrf_exempt
def click_to_edit_cancel(request):
    """
    Handles cancel and returns the original display span.
    """
    value = request.GET.get("value", "This is editable text. Click to edit.")
    return render(request, "demo/click-to-edit-save.html", {"value": value})




def data_table_rows(request):
    """
    Returns the table rows fragment for the data table example.
    Supports sorting and pagination via query params.
    """
    # Demo data
    data = [
        {"name": "Alice", "age": 28, "role": "Developer"},
        {"name": "Bob", "age": 34, "role": "Designer"},
        {"name": "Charlie", "age": 25, "role": "Manager"},
        {"name": "Lana", "age": 30, "role": "Developer"},
        {"name": "Eve", "age": 29, "role": "QA"},
        {"name": "Frank", "age": 32, "role": "Support"},
        {"name": "Grace", "age": 27, "role": "Developer"},
        {"name": "Hank", "age": 31, "role": "Designer"},
        {"name": "Ivy", "age": 26, "role": "Manager"},
        {"name": "Jack", "age": 33, "role": "Developer"},
    ]

    # Get query params
    sort = request.GET.get("sort", "name")
    order = request.GET.get("order", "asc")
    page = int(request.GET.get("page", "1"))
    per_page = 4

    # Sorting
    reverse = (order == "desc")
    if sort in ["name", "age", "role"]:
        data = sorted(data, key=lambda x: x[sort], reverse=reverse)

    # Pagination
    total = len(data)
    start = (page - 1) * per_page
    end = start + per_page
    page_data = data[start:end]
    total_pages = (total + per_page - 1) // per_page

    # Create a page_range for pagination (1-based)
    page_range = list(range(1, total_pages + 1))

    # Render the fragment
    return render(
        request,
        "demo/data-table-rows.html",
        {
            "rows": page_data,
            "sort": sort,
            "order": order,
            "page": page,
            "total_pages": total_pages,
            "page_range": page_range,
        }
    )


def sort_table(request):
    """
    Returns a table fragment with sortable columns using HTMX.
    """
    # Demo data
    data = [
        {"name": "Alice", "age": 28, "role": "Developer"},
        {"name": "Bob", "age": 34, "role": "Designer"},
        {"name": "Charlie", "age": 25, "role": "Manager"},
        {"name": "Lana", "age": 30, "role": "Developer"},
        {"name": "Eve", "age": 29, "role": "QA"},
        {"name": "Frank", "age": 32, "role": "Support"},
        {"name": "Grace", "age": 27, "role": "Developer"},
        {"name": "Hank", "age": 31, "role": "Designer"},
        {"name": "Ivy", "age": 26, "role": "Manager"},
        {"name": "Jack", "age": 33, "role": "Developer"},
    ]

    col_list = ["name", "age", "role"]

    sort = request.GET.get("sort", "name")
    order = request.GET.get("order", "asc")
    reverse = (order == "desc")
    if sort in col_list:
        data = sorted(data, key=lambda x: x[sort], reverse=reverse)

    # Always render the full page, but if HX-Request, only return the fragment
    if request.GET.get("fragment") == "1":
        return render(request, "demo/sort-table-fragment.html", {
            "rows": data,
            "sort": sort,
            "order": order,
            "col_list": col_list,
        })
    return render(request, "demo/sort-table.html", {
        "rows": data,
        "sort": sort,
        "order": order,
        "col_list": col_list,
    })

def dynamic_form_validation(request):
    print(request)
    """
    Server-side validation for the Dynamic Form Validation example.
    Returns HTML with validation messages for username and email.
    """
    username = request.POST.get('username', '').strip()
    email = request.POST.get('email', '').strip()
    messages = []

    # Username validation
    if not username:
        messages.append('<div class="notification is-danger is-light mb-2">Username is required.</div>')
    elif len(username) < 3:
        messages.append('<div class="notification is-danger is-light mb-2">Username must be at least 3 characters.</div>')
    else:
        messages.append('<div class="notification is-success is-light mb-2">Username looks good!</div>')

    # Email validation
    import re
    email_regex = r'^[^@]+@[^@]+\.[^@]+$'
    if not email:
        messages.append('<div class="notification is-danger is-light mb-2">Email is required.</div>')
    elif not re.match(email_regex, email):
        messages.append('<div class="notification is-danger is-light mb-2">Please enter a valid email address.</div>')
    else:
        messages.append('<div class="notification is-success is-light mb-2">Email looks good!</div>')

    html = ''.join(messages)
    return HttpResponse(html)

def live_search_suggestions(request):
    """
    Returns HTML fragment with autocomplete suggestions for live search.
    """
    q = request.GET.get('q', '').strip().lower()
    all_names = [
        "Alice Johnson",
        "Bob Smith",
        "Charlie Brown",
        "Lana White",
        "Eve Black",
        "Frank Green",
        "Grace Hopper",
        "Hank Moody",
        "Ivy Blue",
        "Jack Sparrow"
    ]
    matches = [name for name in all_names if q and q in name.lower()]
    context = {
        "matches": matches,
        "q": q,
    }
    return render(request, "demo/live-search-suggestions.html", context)


def active_search_results(request):
    """
    Returns HTML fragment with live search results for the active search example.
    """
    q = request.GET.get('q', '').strip().lower()
    all_names = [
        "Alice Johnson",
        "Bob Smith",
        "Charlie Brown",
        "Lana White",
        "Eve Black",
        "Frank Green",
        "Grace Hopper",
        "Hank Moody",
        "Ivy Blue",
        "Jack Sparrow"
    ]
    matches = [name for name in all_names if q and q in name.lower()]
    context = {
        "matches": matches,
        "q": q,
    }
    return render(request, "demo/active-search-results.html", context)



def infinite_scroll_items(request):
    """
    Returns HTML fragment for infinite scroll items.
    """
    # Demo: 15 items, 10 per page
    import time
    time.sleep(.1)

    total_items = 150
    items_per_page = 10
    page = int(request.GET.get("page", "1"))
    start = (page - 1) * items_per_page + 1
    end = min(page * items_per_page, total_items)
    items = [f"Item {i}" for i in range(start, end + 1)]
    has_more = end < total_items
    context = {
        "items": items,
        "next_page": page + 1,
        "has_more": has_more,
    }
    return render(request, "demo/infinite-scroll-items.html", context)

def master_detail_detail(request):
    """
    Returns the detail fragment for the Master/Detail example.
    """
    id = request.GET.get("id", "1")
    details = {
        "1": {
            "name": "Alice Johnson",
            "role": "Developer",
            "email": "alice@example.com",
            "bio": "Alice is a full-stack developer with 5 years of experience in JavaScript and Python.",
            "icon": "fas fa-user-astronaut",
            "image": "https://randomuser.me/api/portraits/women/1.jpg"
        },
        "2": {
            "name": "Bob Smith",
            "role": "Designer",
            "email": "bob@example.com",
            "bio": "Bob is a creative designer who loves crafting beautiful user interfaces.",
            "icon": "fas fa-paint-brush",
            "image": "https://randomuser.me/api/portraits/men/2.jpg"
        },
        "3": {
            "name": "Charlie Brown",
            "role": "Manager",
            "email": "charlie@example.com",
            "bio": "Charlie manages the team and ensures projects are delivered on time.",
            "icon": "fas fa-user-tie",
            "image": "https://randomuser.me/api/portraits/men/3.jpg"
        },
        "4": {
            "name": "Lana White",
            "role": "Developer",
            "email": "lana@example.com",
            "bio": "Lana specializes in backend development and database design.",
            "icon": "fas fa-database",
            "image": "https://randomuser.me/api/portraits/women/4.jpg"
        }
    }
    d = details.get(id, {
        "name": "Unknown",
        "role": "",
        "email": "",
        "bio": "No details available.",
        "icon": "fas fa-question-circle",
        "image": "https://randomuser.me/api/portraits/lego/1.jpg"
    })
    return render(request, "demo/master-detail-detail.html", {"d": d})


def dependent_dropdown_options(request):
    """
    Returns the options for the dependent dropdown based on the selected category.
    """
    category = request.GET.get("category", "")
    options = {
        "fruits": [
            ("apple", "Apple"),
            ("banana", "Banana"),
            ("orange", "Orange"),
            ("pear", "Pear"),
        ],
        "vegetables": [
            ("carrot", "Carrot"),
            ("broccoli", "Broccoli"),
            ("lettuce", "Lettuce"),
            ("spinach", "Spinach"),
        ],
        "animals": [
            ("cat", "Cat"),
            ("dog", "Dog"),
            ("elephant", "Elephant"),
            ("lion", "Lion"),
        ],
    }
    return render(request, "demo/dependent-dropdown-options.html", {
        "items": options.get(category, []),
    })

def tab_content(request):
    """
    Returns the content for a given tab in the tabbed interface example.
    """
    tab = request.GET.get("tab", "overview")
    tab_contents = {
        "overview": {
            "title": "Overview",
            "body": "This is the overview tab. It provides a summary of the content."
        },
        "details": {
            "title": "Details",
            "body": "This is the details tab. Here you can find more in-depth information."
        },
        "settings": {
            "title": "Settings",
            "body": "This is the settings tab. Adjust your preferences here."
        }
    }
    content = tab_contents.get(tab, tab_contents["overview"])
    return render(request, "demo/tab-content.html", {"tab": tab, "content": content})

def lazy_load_image(request):
    """
    Returns the actual image tag for lazy loading.
    """
    # For demo, use a static set of images based on a query param
    img_id = request.GET.get("img", "1")
    images = {
        "1": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=400",
        "2": "https://images.unsplash.com/photo-1465101046530-73398c7f28ca?w=400",
        "3": "https://images.unsplash.com/photo-1519125323398-675f0ddb6308?w=400",
        "4": "https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?w=400",
        "5": "https://images.unsplash.com/photo-1750797490751-1fc372fdcf88?w=400",
        "6": "https://images.unsplash.com/photo-1712695148069-f0543f8b0c0a?w=400",
    }
    url = images.get(img_id, images["1"])
    return render(request, "demo/lazy-load-image.html", {"url": url, "img_id": img_id})

@csrf_exempt
def delete_row(request):
    """
    Handles AJAX row deletion for the Delete Row example.
    """
    row_id = request.POST.get("row_id")
    # In a real app, delete from DB here.
    # For demo, just return an empty response to remove the row.
    return HttpResponse("")

def progress_bar(request):
    """
    Simulate a long-running AJAX request and return a completion message.
    """
    # Simulate a long-running task
    import time
    time.sleep(3)
    return render(request, "demo/progress-bar-result.html")

def modal_content(request):
    """
    Returns the content for the modal dialog example.
    """
    return render(request, "demo/modal-dialog-content.html")


def theme_switcher(request):
    """
    Returns the theme CSS variables for the selected theme.
    """
    theme = request.GET.get("theme", "light")
    if theme == "dark":
        css_vars = """
        :root {
            --primary-gradient: linear-gradient(135deg, #232526 0%, #414345 100%);
            --secondary-gradient: linear-gradient(135deg, #232526 0%, #4b6cb7 100%);
            --dark-blue: #181a1b;
            --light-gray: #232526;
            --text-color: #f8f9fa;
            --card-bg: #232526;
        }
        body { background: #181a1b; color: #f8f9fa; }
        .box, .card, .navbar, .modal-content { background: #232526 !important; color: #f8f9fa !important; }
        """
    else:
        css_vars = """
        :root {
            --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            --dark-blue: #2c3e50;
            --light-gray: #f8f9fa;
            --text-color: #222;
            --card-bg: #fff;
        }
        body { background: #fff; color: #222; }
        .box, .card, .navbar, .modal-content { background: #fff !important; color: #222 !important; }
        """
    return HttpResponse(css_vars, content_type="text/css")

@csrf_exempt
def drag_drop_update(request):
    """
    Receives the new order of items and returns a success response.
    """
    from urllib.parse import unquote_plus, parse_qs

    if request.method == "POST":
        # If request.body is not empty, parse as form-encoded
        if request.body:
            # Decode bytes to string
            body_str = request.body.decode()
            # Parse params=... from form-encoded body
            parsed = parse_qs(body_str)
            params_json = parsed.get("params", [None])[0]
            if params_json:
                # URL-decode and parse JSON
                params = json.loads(unquote_plus(params_json))
                order = params.get("order", [])
            else:
                order = []

        else:
            # Fallback for form-encoded (should not happen in this example)
            order = request.POST.getlist("order[]")
        return render(request, "demo/drag-drop-update.html", {"order": order})
    return JsonResponse({"success": False}, status=400)


def calendar_month(request):
    """
    Returns a calendar month grid with events for the given month/year.
    """
    year = int(request.GET.get("year", datetime.date.today().year))
    month = int(request.GET.get("month", datetime.date.today().month))
    cal = calendar.Calendar()
    month_days = cal.monthdatescalendar(year, month)

    # Demo events: just a few hardcoded for demo
    events = {
        datetime.date(year, month, 3): "Team Meeting",
        datetime.date(year, month, 10): "Project Deadline",
        datetime.date(year, month, 15): "Birthday 🎂",
        datetime.date(year, month, 22): "Conference",
    }
    days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    return render(request, "demo/calendar-month.html", {
        "year": year,
        "month": month,
        "month_days": month_days,
        "events": events,
        "month_name": calendar.month_name[month],
        "days_of_week": days_of_week,
    })

def polling_example(request):
    """
    Returns a fragment with a random number and the current time for polling demo.
    """
    import datetime
    now = datetime.datetime.now()
    return render(request, "demo/polling-fragment.html", {
        "now": now.strftime("%H:%M:%S"),
        "random_number": random.randint(1, 100),
    })


@csrf_exempt
def csv_export(request):
    """
    Returns a CSV file for the table data.
    """
    if request.method == "POST" and request.POST.get("table_json"):
        try:
            data = json.loads(request.POST["table_json"])
        except Exception:
            data = []
    else:
        # Fallback to demo data
        data = [
            {"name": "Alice", "age": 28, "role": "Developer"},
            {"name": "Bob", "age": 34, "role": "Designer"},
            {"name": "Charlie", "age": 25, "role": "Manager"},
            {"name": "Lana", "age": 30, "role": "Developer"},
            {"name": "Eve", "age": 29, "role": "QA"},
            {"name": "Frank", "age": 32, "role": "Support"},
            {"name": "Grace", "age": 27, "role": "Developer"},
            {"name": "Hank", "age": 31, "role": "Designer"},
            {"name": "Ivy", "age": 26, "role": "Manager"},
            {"name": "Jack", "age": 33, "role": "Developer"},
        ]
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=["name", "age", "role"])
    writer.writeheader()
    for row in data:
        writer.writerow(row)
    # Return as bytes for blob download
    csv_bytes = output.getvalue().encode("utf-8")
    response = HttpResponse(csv_bytes, content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="table-data.csv"'
    return response


def weather_widget(request):
    """
    Returns weather info for a given city using a public API.
    """
    city = request.GET.get("city", "Amsterdam")
    api_key = "demo"  # For demo, use a public test API or mock
    # Use Open-Meteo (no API key required, free and CORS-friendly)
    url = f"https://api.open-meteo.com/v1/forecast?latitude=52.37&longitude=4.89&current_weather=true"
    city_coords = {
        "amsterdam": (52.37, 4.89),
        "london": (51.51, -0.13),
        "paris": (48.85, 2.35),
        "berlin": (52.52, 13.41),
        "new york": (40.71, -74.01),
        "tokyo": (35.68, 139.76),
        "sydney": (-33.87, 151.21),
        "san francisco": (37.77, -122.42),
        "cairo": (30.04, 31.24),
        "cape town": (-33.92, 18.42),
    }
    coords = city_coords.get(city.lower(), city_coords["amsterdam"])
    url = f"https://api.open-meteo.com/v1/forecast?latitude={coords[0]}&longitude={coords[1]}&current_weather=true"
    print(url)
    try:
        resp = requests.get(url, timeout=5)
        data = resp.json()
        weather = data.get("current_weather", {})
        temp = weather.get("temperature")
        wind = weather.get("windspeed")
        code = weather.get("weathercode")
        icon = "fas fa-sun"
        if code in [2, 3, 45, 48]: icon = "fas fa-cloud"
        if code in [51, 53, 55, 61, 63, 65, 80, 81, 82]: icon = "fas fa-cloud-showers-heavy"
        if code in [71, 73, 75, 77, 85, 86]: icon = "fas fa-snowflake"
        if code in [95, 96, 99]: icon = "fas fa-bolt"
        desc = {
            0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
            45: "Fog", 48: "Depositing rime fog", 51: "Light drizzle", 53: "Drizzle",
            55: "Dense drizzle", 61: "Slight rain", 63: "Rain", 65: "Heavy rain",
            71: "Slight snow", 73: "Snow", 75: "Heavy snow", 77: "Snow grains",
            80: "Rain showers", 81: "Heavy showers", 82: "Violent showers",
            85: "Snow showers", 86: "Heavy snow showers", 95: "Thunderstorm",
            96: "Thunderstorm w/ hail", 99: "Thunderstorm w/ heavy hail"
        }.get(code, "Unknown")
    except Exception as e:
        print(e)
        temp = wind = code = None
        icon = "fas fa-question"
        desc = "Could not fetch weather"
    return render(request, "demo/weather-widget-fragment.html", {
        "city": city.title(),
        "temp": temp,
        "wind": wind,
        "desc": desc,
        "icon": icon,
    })

def live_stock_ticker(request):
    hx_trigger = request.headers.get("HX-Trigger")

    try:
        resp = requests.get("https://api.kraken.com/0/public/Ticker", timeout=5)
        data = resp.json()
        price = float(data["result"]["TBTCUSD"]["p"][0].replace(",", ""))
        updated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        price = None
        updated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if hx_trigger == "btc-ticker":
        # Return the HTML fragment.
        return HttpResponse(
            f"""
            <div id="result">
                <div style="font-size: 2.2rem; font-weight: bold;">
                    <i class="fab fa-btc"></i>
                    ${price:,.2f}
                </div>
                <div class="has-text-grey mt-2" style="font-size: 1rem;">
                    Last updated: {updated}
                </div>
            </div>
            """
        )

    return render(request, "demo/live-stock-ticker.html", {
        "price": price,
        "updated": updated,
    })

def markdown_preview(request):
    """
    Returns HTML preview for Markdown input.
    """
    text = request.GET.get("markdown", "")
    html = md.markdown(text, extensions=["extra", "nl2br"])
    return render(request, "demo/markdown-preview-fragment.html", {"html": html})


def color_picker_fragment(request):
    """
    Returns a fragment with a color preview for the selected color.
    """
    color = request.GET.get("color", "#667eea")
    return render(request, "demo/color-picker-fragment.html", {"color": color})


@csrf_exempt
def kanban_board_update(request):
    """
    Receives the new board state for the Kanban board and returns a success response.
    """
    from urllib.parse import unquote_plus, parse_qs
    if request.method == "POST":

        if request.body:
            body_str = request.body.decode()

            parsed = parse_qs(body_str)
            params_json = parsed.get("params", [None])[0]
            print(params_json)
            if params_json:
                # URL-decode and parse JSON
                params = json.loads(unquote_plus(params_json))
                board = params.get("board", {})
            else:
                board = {}

        return render(request, "demo/kanban-board-update.html", {"board": board})
    return JsonResponse({"success": False}, status=400)

@csrf_exempt
def toast_notify(request):
    """
    Returns a toast notification fragment for demo.
    """
    msg = request.POST.get("message", "This is a toast notification!")
    level = request.POST.get("level", "info")
    return render(request, "demo/toast-notification-fragment.html", {"message": msg, "level": level})

def language_switcher(request):
    """
    Returns a fragment with a greeting in the selected language.
    """
    lang = request.GET.get("lang", "en")
    greetings = {
        "en": "Hello, world!",
        "es": "¡Hola, mundo!",
        "fr": "Bonjour le monde!",
        "de": "Hallo Welt!",
        "it": "Ciao mondo!",
        "nl": "Hallo wereld!",
        "zh": "你好，世界！",
        "ja": "こんにちは世界！",
        "ru": "Привет, мир!",
    }
    greeting = greetings.get(lang, greetings["en"])
    return render(request, "demo/language-switcher.html", {"greeting": greeting, "lang": lang})


def reference_api(request):
    return render(request, "frontend/api_reference.html", )