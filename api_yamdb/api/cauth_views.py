from django.contrib.auth import get_user_model
from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny

from .cauth_serializers import SignUpSerialiser

User = get_user_model()


class CreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    pass


class SignUpViewSet(CreateViewSet):
    queryset = User.objects.all()
    serializer_class = SignUpSerialiser
    permission_classes = (AllowAny,)
