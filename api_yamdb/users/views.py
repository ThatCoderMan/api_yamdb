from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User

from .permissions import IsAdmin
from .serializers import SignUpSerializer, TokenSerializer, UserSerializer


def send_email_confirmation(user, confirmation_code):
    subject = f'Подтверждение регистрации пользователя для "{user}"'
    message = (
        'Используйте код подтверждения, чтобы получить токен.\n'
        f'Confirmation code: {confirmation_code}'
    )
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email, ])


class TokenView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(User,
                                     username=serializer.data['username'])
            if user.confirmation_code == serializer.data['confirmation_code']:
                return Response(
                    {'token': str(RefreshToken.for_user(user).access_token)},
                    status=status.HTTP_200_OK
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignUpView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(username=serializer.data['username'])
            if not user.confirmation_code:
                confirmation_code = default_token_generator.make_token(user)
                user.confirmation_code = confirmation_code
                user.save()
            else:
                confirmation_code = user.confirmation_code
            send_email_confirmation(user, confirmation_code)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdmin)
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(methods=['get', 'patch'], detail=False,
            permission_classes=(IsAuthenticated,), url_path='me')
    def get_or_patch_me(self, request):
        user = User.objects.get(username=request.user.username)
        if request.method == 'PATCH':
            serializer = UserSerializer(user, data=request.data, partial=True)
            serializer.is_valid()
            if request.user.role == 'user':
                serializer.validated_data['role'] = 'user'
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
