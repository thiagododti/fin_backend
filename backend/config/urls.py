from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
    TokenBlacklistView
)


from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView
)

urlpatterns = [
    path('api/', include('apps.users.urls')),

    # JWT Auth
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/token/blacklist/', TokenBlacklistView.as_view(),
         name='token_blacklist'),

    # Swagger UI
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'),
         name='swagger-ui'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
]


if settings.DEBUG:
    if getattr(settings, "MEDIA_URL", None) and getattr(settings, "MEDIA_ROOT", None):
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)

    if getattr(settings, "STATIC_URL", None) and getattr(settings, "STATIC_ROOT", None):
        urlpatterns += static(settings.STATIC_URL,
                              document_root=settings.STATIC_ROOT)
