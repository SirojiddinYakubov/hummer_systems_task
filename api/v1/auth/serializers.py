from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from users.models import CustomUser


class LoginSerializer(serializers.Serializer):
    phone_number = PhoneNumberField(required=True)
    password = serializers.CharField(required=False)
    invite_code = serializers.CharField(required=False)


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['phone_number']


class VerifyCodeSerializer(serializers.Serializer):
    phone_number = PhoneNumberField(required=True)
    code = serializers.IntegerField()


class GetCodeSerializer(serializers.Serializer):
    phone_number = PhoneNumberField(required=True)
