from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from reviews.models import User

from .cauth_serializers import SignUpSerialiser


def send_email_confirmation(user, confirmation_code):
    subject = f'Confirmation of user registration for "{user}"'
    message = (
        'Use the confirmation code to get the token.\n'
        f'Confirmation code: {confirmation_code}'
    )
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email, ])


class SignUpViewSet(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignUpSerialiser(data=request.data)
        if serializer.is_valid(raise_exception=True):
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
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


