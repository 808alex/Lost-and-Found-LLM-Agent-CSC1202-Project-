from django.urls import path

from . import views

app_name = "items"

urlpatterns = [
    path("", views.home, name="home"),
    path("report/<str:kind>/", views.report, name="report"),
    path("items/<int:pk>/", views.detail, name="detail"),
]
