from django.urls import path

from . import views

# Use an app name to provide namespacing
app_name = "data"

urlpatterns = [
    path("", views.home, name="home"),
    path("upload/", views.upload, name="upload"),
    path("view/", views.view, name="view"),
]
