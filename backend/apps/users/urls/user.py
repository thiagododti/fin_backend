from rest_framework.routers import SimpleRouter
from apps.users.views import UserViewSet


router = SimpleRouter()
router.register("users", UserViewSet, basename="users")

urlpatterns = router.urls
