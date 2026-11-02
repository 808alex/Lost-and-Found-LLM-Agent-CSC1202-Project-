from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Item


class ReportTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("alice", password="pw-test-123")

    def test_home_loads(self):
        self.assertEqual(self.client.get(reverse("items:home")).status_code, 200)

    def test_report_requires_login(self):
        response = self.client.get(reverse("items:report", args=["lost"]))
        self.assertRedirects(response, "/accounts/login/?next=/report/lost/")

    def test_report_found_item(self):
        self.client.login(username="alice", password="pw-test-123")
        response = self.client.post(
            reverse("items:report", args=["found"]),
            {"description": "Black Nike backpack", "location": "Library", "date": "2026-11-01"},
        )
        item = Item.objects.get()
        self.assertRedirects(response, reverse("items:detail", args=[item.pk]))
        self.assertEqual(item.kind, Item.Kind.FOUND)
        self.assertEqual(item.reported_by, self.user)

    def test_bad_kind_404s(self):
        self.client.login(username="alice", password="pw-test-123")
        self.assertEqual(self.client.get("/report/stolen/").status_code, 404)

    def test_signup_logs_in(self):
        self.client.post(
            reverse("signup"),
            {"username": "bob", "password1": "Sup3r-secret!", "password2": "Sup3r-secret!"},
        )
        response = self.client.get(reverse("items:home"))
        self.assertContains(response, "Log out (bob)")
