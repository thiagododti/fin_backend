from rest_framework.views import exception_handler
from django.http import Http404
from rest_framework.exceptions import NotFound


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        return response

    view = context.get("view")

    if isinstance(exc, (Http404, NotFound)) and view:
        pk = view.kwargs.get("pk")

        if pk is not None and hasattr(view, "get_queryset"):
            model = view.get_queryset().model
            verbose_name = model._meta.verbose_name

            response.data["detail"] = (
                f"{verbose_name.capitalize()} id: {pk} não encontrado."
            )

    return response
