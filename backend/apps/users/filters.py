import django_filters
from django.db.models import Q
from apps.users.models import User


class UserFilter(django_filters.FilterSet):
    full_name = django_filters.CharFilter(method="filter_full_name")
    email = django_filters.CharFilter(field_name="email", lookup_expr="icontains")
    username = django_filters.CharFilter(field_name="username", lookup_expr="icontains")

    class Meta:
        model = User
        fields = ["username", "email", "full_name"]

    def filter_full_name(self, queryset, name, value):
        parts = value.split()

        if len(parts) == 1:
            return queryset.filter(
                Q(first_name__icontains=parts[0]) | Q(last_name__icontains=parts[0])
            )

        return queryset.filter(
            first_name__icontains=parts[0], last_name__icontains=parts[-1]
        )
