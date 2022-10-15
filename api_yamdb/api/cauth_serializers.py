import re


from rest_framework.serializers import ModelSerializer
from rest_framework import validators


from reviews.models import User

REGEX_USERNAME = r'^[\w.@+-]+$'


class SignUpSerialiser(ModelSerializer):
    # email = EmailField(
    #     source='user.email',
    #     validators=(UniqueValidator(queryset=User.objects.all()),)
    # )
    # username = CharField(
    #     source='user.username',
    #     validators=(UniqueValidator(queryset=User.objects.all()),)
    # )

    class Meta:
        model = User
        fields = ('username', 'email',)

    # def run_validators(self, value):
    #     for validator in self.validators:
    #         if isinstance(validator, validators.UniqueTogetherValidator):
    #             self.validators.remove(validator)
    #     super(SignUpSerialiser, self).run_validators(value)
    #
    # def create(self, validated_data):
    #     instance, _ = User.objects.get_or_create(**validated_data)
    #     return instance
