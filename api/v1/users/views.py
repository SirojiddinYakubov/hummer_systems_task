from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.v1.users.serializers import UserSerializer, SetPasswordSerializer
from users.models import CustomUser


class UsersList(generics.ListAPIView):
    queryset = CustomUser.objects.exclude(is_superuser=True)
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['phone_number', 'invite_code__code']


class UsersMe(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)


class SetPassword(generics.GenericAPIView):
    serializer_class = SetPasswordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data.get('password')

        user = request.user
        user.set_password(password)
        user.save()
        return Response({"message": "Password successfully changed!"})
