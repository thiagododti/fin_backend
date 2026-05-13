from rest_framework import serializers
from apps.users.models import User
from django.contrib.auth.password_validation import validate_password


class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "last_login",
            "is_superuser",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_staff",
            "is_active",
            "date_joined",
            "birth_date",
            "photo",
        ]


class ReadUserSerializer(BaseUserSerializer):
    pass


class WriteUserSerializer(BaseUserSerializer):
    password = serializers.CharField(
        write_only=True, required=False, min_length=8, style={"input_type": "password"}
    )
    password2 = serializers.CharField(
        write_only=True, required=False, min_length=8, style={"input_type": "password"}
    )

    class Meta(BaseUserSerializer.Meta):
        fields = BaseUserSerializer.Meta.fields + [
            "password",
            "password2",
        ]

    def validate(self, data):  # type: ignore
        password = data.get("password")
        password2 = data.get("password2")

        if password or password2:
            if password != password2:
                raise serializers.ValidationError("As senhas não coincidem.")

        return data

    def validate_password(self, value):
        validate_password(value, self.instance or User())
        return value

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields["password"].required = False
            self.fields["password2"].required = False
        else:
            self.fields["password"].required = True
            self.fields["password2"].required = True

    def create(self, validated_data):
        password = validated_data.pop("password")
        validated_data.pop("password2", None)
        return User.objects.create_user(password=password, **validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        validated_data.pop("password2", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance

    @staticmethod
    def validate_photo(value):
        max_size = 2 * 1024 * 1024  # 2MB
        if value.size > max_size:
            raise serializers.ValidationError("A imagem não pode ser maior que 2MB.")
        return value


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value

    def validate(self, data):  # type: ignore
        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError("As novas senhas não coincidem.")
        return data


class ProfileSerializer(serializers.ModelSerializer):
    """Usuário visualiza e edita o próprio perfil."""

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "birth_date",
            "photo",
        ]
        read_only_fields = ["id"]

    @staticmethod
    def validate_photo(value):
        if value.size > 2 * 1024 * 1024:
            raise serializers.ValidationError("A imagem não pode ser maior que 2MB.")
        return value


class RegistrationSerializer(serializers.ModelSerializer):
    """Auto-cadastro público — sem campos de administração."""

    password = serializers.CharField(
        write_only=True, min_length=8, style={"input_type": "password"}
    )
    password2 = serializers.CharField(
        write_only=True, min_length=8, style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "birth_date",
            "password",
            "password2",
        ]

    def validate_password(self, value):
        validate_password(value)
        return value

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError("As senhas não coincidem.")
        return data

    def create(self, validated_data):
        validated_data.pop("password2")
        password = validated_data.pop("password")
        return User.objects.create_user(password=password, **validated_data)
