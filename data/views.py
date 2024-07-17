import os

from django import forms
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from .logic import *
from .models import *

# Allows app name to be easily changed when merging into another project
app_name = "data"


def home(request):
    context = {}
    context["username"] = os.getenv("DJANGO_SUPERUSER_USERNAME")
    context["password"] = os.getenv("DJANGO_SUPERUSER_PASSWORD")

    template = f"{app_name}/home.html"

    return render(request, template, context)


class UploadForm(forms.ModelForm):

    class Meta:
        model = Upload
        fields = ["file", "field_mapping", "description"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3, "cols": 80}),
        }

    # Only accept supported file types
    def clean_file(self):
        file = self.cleaned_data.get("file")

        allowed_file_types = tuple(CodecStrategy.extensions)

        if not file.name.endswith(allowed_file_types):
            raise forms.ValidationError(
                "Only the following file types are currently supported: "
                + ", ".join(allowed_file_types)
            )

        return file


def upload_data(request):
    context = {}
    template = f"{app_name}/upload_data.html"

    context["supported_codec_names"] = CodecStrategy.names

    check_mappings_exist()

    if request.method == "POST":
        upload_form = UploadForm(request.POST, request.FILES)

        if upload_form.is_valid():

            upload_instance = upload_form.save(commit=False)

            # Attempt to process the data
            # For demonstration purposes we will do this synchronously
            # In a production environment, this might be done asynchronously
            upload_result = process_upload(upload_instance, request.FILES["file"])

            if upload_result == "success":

                if request.user.is_authenticated:
                    upload_instance.uploaded_by = request.user

                upload_instance.save()

                # Always redirect successful forms to avoid form resubmission if user refreshes the page
                url = reverse(f"{app_name}:view_data")
                query_params = "?status=success"
                return redirect(f"{url}{query_params}")

            else:

                context["upload_result"] = upload_result
    else:
        upload_form = UploadForm()

    context["upload_form"] = upload_form

    return render(request, template, context)


def view_data(request):
    context = {}

    codec_names = CodecStrategy.names
    extensions = CodecStrategy.extensions
    mime_types = CodecStrategy.mime_types

    context["supported_codecs"] = zip(codec_names, extensions, mime_types)

    context["data_count"] = Data.objects.all().count()

    template = f"{app_name}/view_data.html"

    return render(request, template, context)


def download_data(request):

    type = request.GET.get("type", None)

    data_out, mime_type, extension = get_data_for_download(type, None)

    response = HttpResponse(data_out, content_type=mime_type)
    response["Content-Disposition"] = f"attachment; filename=data.{extension}"

    return response
