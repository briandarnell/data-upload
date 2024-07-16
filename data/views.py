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
    template = f"{app_name}/home.html"

    return render(request, template, context)


class UploadForm(forms.ModelForm):

    class Meta:
        model = Upload
        fields = ["file", "field_mapping", "description"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3, "cols": 80}),
        }

    # Only accept .csv and .json files
    def clean_file(self):
        file = self.cleaned_data.get("file")

        allowed_file_types = tuple(CodecStrategy.file_types)

        if not file.name.endswith(allowed_file_types):
            raise forms.ValidationError(
                "Only the following file types are currently supported:"
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

            # Now process the data
            # For demonstration we will do this synchronously
            # In a production environment, this might be done asynchronously
            upload_result = process_upload(upload_instance, request.FILES["file"])

            if upload_result == "success":

                if request.user.is_authenticated:
                    upload_instance.uploaded_by = request.user

                try:
                    upload_instance.save()
                    # Always redirect successful forms to avoid form resubmission on page refresh
                    url = reverse(f"{app_name}:view")
                    query_params = "?status=success"
                    return redirect(f"{url}{query_params}")

                except IntegrityError as e:
                    # This is a duplicate file condition
                    context["upload_result"] = (
                        f"The file {upload_instance.file.name} has already been uploaded (hash: {upload_instance.file_hash})."
                    )

            else:

                context["upload_result"] = upload_result

    upload_form = UploadForm()

    context["upload_form"] = upload_form

    return render(request, template, context)


def view_data(request):
    context = {}

    codec_names = CodecStrategy.names
    extensions = CodecStrategy.extensions
    mime_types = CodecStrategy.mime_types

    context["supported_codecs"] = zip(codec_names, extensions, mime_types)

    template = f"{app_name}/view_data.html"

    return render(request, template, context)


def download_data(request):

    type = request.GET.get("type", None)

    if type is None:
        type = "json"

    codec_class = CodecStrategy.get_subclass_from_extension(type)
    codec = codec_class()

    # For demonstration purposes, we will just get the first mapping
    # In a production environment, the user might have to select the mapping
    mapping = FieldMapping.objects.first().mapping
    reverse_mapping = {db: file for file, db in mapping.items()}

    field_list = [db for file, db in mapping.items()]
    print(field_list)

    data = list(Data.objects.all().values(*field_list))

    print(data)
    data_with_mapping = replace_keys_in_list_of_dicts(data, reverse_mapping)
    print(data_with_mapping)

    data_out = codec.from_dict(data_with_mapping)

    response = HttpResponse(data_out, content_type=codec.mime_type)
    response["Content-Disposition"] = f"attachment; filename=data.{codec.extension}"

    return response
