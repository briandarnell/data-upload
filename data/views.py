from django.shortcuts import render

# Allows app name to be easily changed when merging into another project
app_name = "data"


def home(request):
    context = {}
    template = f"{app_name}/home.html"

    return render(request, template, context)


def upload(request):
    context = {}
    template = f"{app_name}/upload.html"

    return render(request, template, context)


def view(request):
    context = {}
    template = f"{app_name}/view.html"

    return render(request, template, context)
