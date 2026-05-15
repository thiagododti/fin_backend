from rest_framework.exceptions import MethodNotAllowed


class BlockPutMixin:
    """Mixin que bloqueia requisições PUT, aceitando apenas PATCH para atualização."""

    def update(self, request, *args, **kwargs):
        if request.method.upper() == "PUT":
            raise MethodNotAllowed(
                "PUT",
                detail="Metodo PUT não permitido. Use PATCH para atualização parcial.",
            )
        return super().update(request, *args, **kwargs)
