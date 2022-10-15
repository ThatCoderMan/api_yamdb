import hashlib
import random
import re

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework.serializers import (CharField, EmailField, ModelSerializer,
                                        ValidationError)
from rest_framework.validators import UniqueValidator

REGEX_USERNAME = r'^[\w.@+-]+$'

User = get_user_model()


class SignUpSerialiser(ModelSerializer):
    email = EmailField(
        source='user.email',
        validators=(UniqueValidator(queryset=User.objects.all()),)
    )
    username = CharField(
        source='user.username',
        validators=(UniqueValidator(queryset=User.objects.all()),)
    )

    class Meta:
        model = User
        fields = ('username', 'email',)

    def validate_username(self, value):
        is_regex = bool(re.match(REGEX_USERNAME, value))
        if not is_regex or (value.lower() == 'me'):
            raise ValidationError(
                'Using \'me\' as a value of \'username\' is fobbiden.'
            )
        return value

    def get_confirm_code(self, email):
        return hashlib.sha256(
            str(random.random()) + email
        ).encode('utf-8').hexdigest()[:20]

    def send_email_confirmation(self, user, confirmation_code):
        subject = f'Confirmation of user registration for "{user}"'
        message = (
            'Use the confirmation code to get the token.\n'
            f'Confirmation code: {confirmation_code}'
        )
        send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email, ])

    def create(self, validated_data):
        username = validated_data.get('username')
        email = validated_data.get('username')
        try:
            user = User.objects.get(username=username)
            if email != user.email:
                raise ValidationError(
                    'Requested \'email\' doesn\'t match account \'email\''
                )
            confirmation_code = self.get_confirm_code(user.email)
        except user.DoesNotExist:
            email = validated_data.get('email')
            confirmation_code = self.get_confirm_code(email)
            user = User.objects.create(
                **validated_data,
                confirmation_code=confirmation_code
            )
        finally:
            self.send_email_confirmation(user, confirmation_code)
        return user
