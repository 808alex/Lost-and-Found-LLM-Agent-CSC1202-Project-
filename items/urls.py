from django.urls import path

from . import views

app_name = "items"

urlpatterns = [
    path("lost-and-found/", views.home, name="home"),
    path("find/", views.find, name="find"),
    path("find/results/", views.results, name="results"),
    path("report/", views.report, name="report"),
    path("items/<int:pk>/", views.detail, name="detail"),
]
