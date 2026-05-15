from apps.users.models import User


class InvalidCurrentPassword(Exception):
    pass


def create_user(password: str, **data) -> User:
    return User.objects.create_user(password=password, **data)


def update_user(instance: User, password: str | None = None, **data) -> User:
    for attr, value in data.items():
        setattr(instance, attr, value)
    if password:
        instance.set_password(password)
    instance.save()
    return instance


def change_password(user: User, current_password: str, new_password: str) -> None:
    if not user.check_password(current_password):
        raise InvalidCurrentPassword("Senha atual incorreta.")
    user.set_password(new_password)
    user.save(update_fields=["password"])
