from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import SignUpView, TokenView, UserViewSet

router = SimpleRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/auth/signup/', SignUpView.as_view()),
    path('api/v1/auth/token/', TokenView.as_view()),
]
