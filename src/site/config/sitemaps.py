from django.contrib import sitemaps
from django.urls import reverse


class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = "weekly"

    def items(self):
        return ["index", "documentation", "examples", "reference"]

    def location(self, item):
        return reverse(item)

import json
from django.conf import settings

class ExampleSitemap(sitemaps.Sitemap):
    priority = 0.6
    changefreq = "weekly"

    def items(self):
        # Load all example IDs from your JSON file
        examples_path = settings.BASE_DIR / "main" / "examples.json"
        with open(examples_path, "r") as f:
            examples = json.load(f)
        return [ex["id"] for ex in examples]

    def location(self, item):
        # Return the direct URL for each example
        return f"/examples/{item}"