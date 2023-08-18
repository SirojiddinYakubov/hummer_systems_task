from rest_framework import serializers

from users.models import CustomUser, InviteCode


class InviteCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InviteCode
        fields = ['code']


class UserSerializer(serializers.ModelSerializer):
    invite_code = InviteCodeSerializer()

    class Meta:
        model = CustomUser
        fields = ['id', 'phone_number', 'invite_code']


class SetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField()
