from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Item


class ReportTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("alice", password="pw-test-123")

    def test_home_requires_login(self):
        self.assertRedirects(self.client.get(reverse("items:home")), "/?next=/lost-and-found/")

    def test_home_loads_when_logged_in(self):
        self.client.login(username="alice", password="pw-test-123")
        self.assertContains(self.client.get(reverse("items:home")), "Hi alice")

    def test_login_is_first_page(self):
        response = self.client.post("/", {"username": "alice", "password": "pw-test-123"})
        self.assertRedirects(response, reverse("items:home"))

    def test_logged_in_user_skips_login(self):
        self.client.login(username="alice", password="pw-test-123")
        self.assertRedirects(self.client.get("/"), reverse("items:home"))

    def test_login_page_has_no_signup(self):
        self.assertNotContains(self.client.get(reverse("login")), "Sign up")

    def test_report_requires_login(self):
        response = self.client.get(reverse("items:report"))
        self.assertRedirects(response, "/?next=/report/")

    def test_report_lost_item(self):
        self.client.login(username="alice", password="pw-test-123")
        response = self.client.post(
            reverse("items:report"),
            {"description": "Black Nike backpack", "location": "Library", "date": "2026-11-01"},
        )
        item = Item.objects.get()
        self.assertRedirects(response, reverse("items:detail", args=[item.pk]))
        self.assertEqual(item.kind, Item.Kind.LOST)
        self.assertEqual(item.reported_by, self.user)

    def test_report_fills_in_attributes(self):
        self.client.login(username="alice", password="pw-test-123")
        self.client.post(
            reverse("items:report"),
            {"description": "Black Nike backpack", "location": "Library", "date": "2026-11-01"},
        )
        item = Item.objects.get()
        self.assertEqual(item.object_type, "bag")
        self.assertEqual(item.colour, "black")

    def test_no_report_found_page(self):
        self.client.login(username="alice", password="pw-test-123")
        self.assertEqual(self.client.get("/report/found/").status_code, 404)


class FindTests(TestCase):
    def setUp(self):
        user = User.objects.create_user("alice", password="pw-test-123")
        self.client.login(username="alice", password="pw-test-123")
        common = {"kind": "found", "date": "2026-11-01", "reported_by": user}
        self.backpack = Item.objects.create(
            description="Black Nike backpack", object_type="bag", colour="black", location="Library", **common
        )
        self.phone = Item.objects.create(
            description="Blue iPhone in a clear case", object_type="phone", colour="blue", location="The Helix", **common
        )
        Item.objects.create(
            description="Black wallet", object_type="wallet", colour="black", **{**common, "kind": "lost"}
        )

    def find(self, **params):
        return self.client.get(reverse("items:results"), params).context["results"]

    def test_find_page_sends_to_results_page(self):
        self.assertContains(self.client.get(reverse("items:find")), f'action="{reverse("items:results")}"')

    def test_empty_search_goes_back_to_find(self):
        self.assertRedirects(self.client.get(reverse("items:results")), reverse("items:find"))

    def test_results_show_what_agent_understood(self):
        response = self.client.get(reverse("items:results"), {"q": "black nike backpack"})
        self.assertContains(response, "Bag / backpack")
        self.assertContains(response, "Black")

    def test_search_by_words(self):
        self.assertEqual(self.find(q="I lost my nike backpack"), [self.backpack])

    def test_filter_by_colour_only_shows_found_items(self):
        self.assertEqual(self.find(colour="black"), [self.backpack])

    def test_filters_and_words_combine(self):
        self.assertEqual(self.find(q="iphone", colour="black"), [])

