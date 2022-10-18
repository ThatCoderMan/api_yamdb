from django.forms import ValidationError


def validate_me_as_username(value: str):
    if value.lower().strip() == 'me':
        raise ValidationError(
            'Использование "me" в качестве "username" недопустимо.',
            params={'username': value},
        )
