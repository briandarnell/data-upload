from django.urls import path

from . import views

# Use an app name to provide namespacing
app_name = "data"

urlpatterns = [
    path("", views.home, name="home"),
    path("upload/", views.upload_data, name="upload_data"),
    path("view/", views.view_data, name="view_data"),
    path("download/", views.download_data, name="download_data"),
]
