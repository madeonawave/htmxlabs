import pytest
from django.urls import reverse
from django.test import Client

@pytest.mark.django_db
class TestExamplesViews:
    @classmethod
    def setup_class(cls):
        cls.client = Client()

    def test_examples_page_loads(self):
        response = self.client.get(reverse("examples"))
        assert response.status_code == 200
        assert b"Examples" in response.content

    def test_example_direct_valid(self):
        # Use a known example id from examples.json, e.g. "basic-ajax"
        response = self.client.get(reverse("example_direct", args=["basic-ajax"]))
        print(response.content)
        assert response.status_code == 200
        assert b"Basic AJAX" in response.content

    def test_example_direct_invalid(self):
        response = self.client.get(reverse("example_direct", args=["not-a-real-example"]))
        assert response.status_code == 404

    def test_dynamic_page_allowed(self):
        # Test a whitelisted demo page
        response = self.client.get(reverse("examples", args=["click-to-edit.html"]))
        assert response.status_code == 200
        assert b"Click to Edit" in response.content

    def test_dynamic_page_not_allowed(self):
        # Test a non-whitelisted page
        response = self.client.get(reverse("examples", args=["not-allowed.html"]))
        assert response.status_code == 404

    def test_like_button_get(self):
        response = self.client.get(reverse("like_button"))
        assert response.status_code == 200
        assert b"Like" in response.content

    def test_live_search_suggestions(self):
        response = self.client.get(reverse("live_search_suggestions"), {"q": "alice"})
        assert response.status_code == 200
        assert b"Alice Johnson" in response.content

    def test_csv_export(self):
        response = self.client.post(reverse("csv_export"))
        assert response.status_code == 200
        assert response["Content-Type"] == "text/csv"
        assert b"name,age,role" in response.content

    def test_theme_switcher_light(self):
        response = self.client.get(reverse("theme_switcher"), {"theme": "light"})
        assert response.status_code == 200
        assert b"--primary-gradient" in response.content

    def test_theme_switcher_dark(self):
        response = self.client.get(reverse("theme_switcher"), {"theme": "dark"})
        assert response.status_code == 200
        assert b"--primary-gradient" in response.content

    def test_data_table_rows(self):
        response = self.client.get(reverse("data_table_rows"))
        assert response.status_code == 200
        assert b"Alice" in response.content
        assert b"Bob" in response.content

    def test_sort_table_fragment(self):
        response = self.client.get(reverse("sort_table"), {"fragment": "1"})
        assert response.status_code == 200
        assert b"table" in response.content

    def test_click_to_edit_form(self):
        response = self.client.get(reverse("click_to_edit_form"), {"value": "Test Edit"})
        assert response.status_code == 200
        assert b"Test Edit" in response.content

    def test_click_to_edit_save(self):
        response = self.client.post(reverse("click_to_edit_save"), {"value": "Saved Value"})
        assert response.status_code == 200
        assert b"Saved Value" in response.content

    def test_click_to_edit_cancel(self):
        response = self.client.get(reverse("click_to_edit_cancel"), {"value": "Cancel Value"})
        assert response.status_code == 200
        assert b"Cancel Value" in response.content

    def test_infinite_scroll_items(self):
        response = self.client.get(reverse("infinite_scroll_items"), {"page": 1})
        assert response.status_code == 200
        assert b"Item 1" in response.content

    def test_tab_content(self):
        response = self.client.get(reverse("tab_content"), {"tab": "details"})
        assert response.status_code == 200
        assert b"details tab" in response.content

    def test_dependent_dropdown_options(self):
        response = self.client.get(reverse("dependent_dropdown_options"), {"category": "fruits"})
        assert response.status_code == 200
        assert b"Apple" in response.content

    def test_htmx_header_returns_fragment(self):
        # Simulate an HTMX request for the contact form fragment
        response = self.client.get(reverse("contact"), HTTP_HX_REQUEST="true")
        assert response.status_code == 200
        # Should return the contact form fragment, not the full page
        assert b"contact_form_fragment" in response.content or b"name" in response.content

    def test_htmx_like_button_post(self):
        # Simulate an HTMX POST to like_button
        response = self.client.post(reverse("like_button"), HTTP_HX_REQUEST="true")
        assert response.status_code == 200
        assert b"Like" in response.content

    def test_htmx_dynamic_form_validation(self):
        # Simulate an HTMX POST for form validation
        response = self.client.post(reverse("dynamic_form_validation"), {"username": "ab", "email": "bademail"}, HTTP_HX_REQUEST="true")
        assert response.status_code == 200
        assert b"Username must be at least 3 characters" in response.content
        assert b"Please enter a valid email address" in response.content

    def test_htmx_modal_content(self):
        response = self.client.get(reverse("modal_content"), HTTP_HX_REQUEST="true")
        assert response.status_code == 200
        assert b"modal" in response.content.lower()
