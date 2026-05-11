from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()


@receiver(post_migrate)
def create_superuser(sender, **kwargs):
    if not settings.TESTING:
        if not User.objects.filter(username="admin").exists():
            print("Iniciando a criação de superuser padrão por Signal, caso deseje remover essa ação remova do arquivo /apps/users/apps a ação do signal!")
            user = User.objects.create_superuser(
                username="admin",
                email="admin@email.com",
                password="admin123",
                first_name="Admin",
                last_name="User",
                birth_date="1990-01-01",
            )
            if user:
                print("Superuser 'admin' created successfully.")
