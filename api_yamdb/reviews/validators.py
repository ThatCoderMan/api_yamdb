from django.forms import ValidationError


def validate_me_as_username(value: str):
    if value.lower().strip() == 'me':
        raise ValidationError(
            'Using "me" as a value of "username" is fobbiden',
            params={'username': value},
        )
