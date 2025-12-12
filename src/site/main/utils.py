from functools import wraps

from django.shortcuts import render


def htmx_template(partial_template, full_template):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            response = view_func(request, *args, **kwargs)

            if hasattr(response, "context_data"):
                context = response.context_data
            else:
                context = {}

            if request.headers.get("HX-Request"):
                return render(request, partial_template, context)
            else:
                return render(request, full_template, context)

        return wrapper

    return decorator
