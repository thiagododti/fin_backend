from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.parsers import MultiPartParser
from rest_framework.decorators import action
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiResponse
from config.serializers import DefaultErrorSerializer

from apps.users.serializers import (
    ReadUserSerializer,
    WriteUserSerializer,
    ChangePasswordSerializer,
    RegistrationSerializer,
    ProfileSerializer,
)
from apps.users.models import User
from apps.users.filters import UserFilter

# Create your views here.


@extend_schema(tags=["Usuários"], description="Operações de CRUD para usuários.")
@extend_schema_view(
    list=extend_schema(
        responses={
            200: ReadUserSerializer(many=True),
            401: OpenApiResponse(
                description="Não autenticado", response=DefaultErrorSerializer
            ),
            403: OpenApiResponse(
                description="Sem permissão", response=DefaultErrorSerializer
            ),
        }
    ),
    retrieve=extend_schema(
        responses={
            200: ReadUserSerializer,
            404: OpenApiResponse(
                description="Usuário não encontrado", response=DefaultErrorSerializer
            ),
        }
    ),
    create=extend_schema(
        responses={
            201: RegistrationSerializer,
            400: OpenApiResponse(
                description="Erro de validação", response=DefaultErrorSerializer
            ),
        }
    ),
)
class UserViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    queryset = User.objects.all()
    filterset_class = UserFilter
    parser_classes = [MultiPartParser]
    serializer_class = WriteUserSerializer

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        if self.action in {"me", "change_password"}:
            return [IsAuthenticated()]
        return [IsAdminUser()]

    def get_serializer_class(self):
        if self.action == "create":
            return RegistrationSerializer
        if self.action == "me":
            return ProfileSerializer
        if self.action in {"list", "retrieve"}:
            return ReadUserSerializer
        return WriteUserSerializer

    @extend_schema(
        methods=["get"],
        responses={200: ProfileSerializer},
    )
    @extend_schema(
        methods=["patch"],
        request=ProfileSerializer,
        responses={
            200: ProfileSerializer,
            400: OpenApiResponse(
                description="Erro de validação", response=DefaultErrorSerializer
            ),
        },
    )
    @action(
        detail=False,
        methods=["get", "patch"],
        url_path="me",
        parser_classes=[MultiPartParser],
    )
    def me(self, request):
        if request.method == "GET":
            return Response(ProfileSerializer(request.user).data)
        serializer = ProfileSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(
        request=ChangePasswordSerializer,
        responses={
            200: OpenApiResponse(description="Senha alterada com sucesso"),
            400: OpenApiResponse(
                description="Erro de validação", response=DefaultErrorSerializer
            ),
        },
    )
    @action(detail=False, methods=["post"], url_path="change-password")
    def change_password(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user

        if not user.check_password(serializer.validated_data["current_password"]):
            return Response(
                {"detail": "Senha atual incorreta."}, status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(serializer.validated_data["new_password"])
        user.save(update_fields=["password"])

        return Response({"detail": "Senha alterada com sucesso."})
