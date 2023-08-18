import pyotp
from django.contrib.auth import authenticate
from django.core.cache import cache
from django.utils.translation import gettext_lazy as _
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from core.message_broker import InfoBipMessageBroker
from core.settings import OTP_EXPIRES_IN
from users.models import CustomUser, InviteCode
from .serializers import LoginSerializer, RegisterSerializer, VerifyCodeSerializer, GetCodeSerializer


class BaseAuthAPIView:
    @classmethod
    def make_response(cls, user):
        refresh = RefreshToken.for_user(user)
        return Response({
            "token_type": "bearer",
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

    @classmethod
    def send_otp(cls, phone_number, message, invite_code=None):
        secret = pyotp.random_base32()
        totp = pyotp.TOTP(secret, digits=4, interval=OTP_EXPIRES_IN)
        code = totp.now()
        message_broker = InfoBipMessageBroker()
        if invite_code:
            message = _(message).format(code=code, invite_code=invite_code)
        else:
            message = _(message).format(code=code)
        message_broker.send_message(str(phone_number), message)
        return secret


class Login(BaseAuthAPIView, generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data.get('phone_number')
        password = serializer.validated_data.get('password')
        invite_code = serializer.validated_data.get('invite_code')

        if password:
            """ Login with password """
            user = authenticate(
                phone_number=phone_number,
                password=password
            )
            if not user:
                return Response({"message": _("Invalid credentials!")}, status=status.HTTP_401_UNAUTHORIZED)

            if not user.is_verified:
                # send otp via message
                secret = self.send_otp(phone_number, "Your confirmation code: {code}")
                cache.set(phone_number, secret, timeout=OTP_EXPIRES_IN)

                return Response({
                    "message": _("Your account not verified! We have sent you a code via SMS to verify your account.")
                }, status=status.HTTP_400_BAD_REQUEST)

        elif invite_code:
            """ Login with invite code """
            try:
                invite_code_obj = InviteCode.objects.get(code=invite_code)
            except InviteCode.DoesNotExist:
                return Response({"message": _("Invite code not found!")})

            try:
                user = CustomUser.objects.get(phone_number=phone_number)
            except CustomUser.DoesNotExist:
                return Response({"message": _("User not found with this phone number!")})

            if user.invite_code:
                return Response({"message": _("You can only activate the invite code 1 time")},
                                status=status.HTTP_400_BAD_REQUEST)

            user.invite_code = invite_code_obj
            user.save()
        else:
            return Response({"message": _("password or invite_code required!")},
                            status=status.HTTP_400_BAD_REQUEST)
        return self.make_response(user)


class Register(BaseAuthAPIView, generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data.get('phone_number')
        user = CustomUser.objects.filter(phone_number=phone_number).last()
        if user:
            return Response({"message": _("User with this phone number already exists!")},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        invite_code = InviteCode.objects.create()

        secret = self.send_otp(phone_number, "Your confirmation code: {code} and invite code: {invite_code}",
                               invite_code.code)
        cache.set(phone_number, secret, timeout=OTP_EXPIRES_IN)

        return Response({"message": _(
            "We send confirmation code and invite code to this phone. Please verify your account and login with invite code!"
        )})


class GetCode(BaseAuthAPIView, generics.GenericAPIView):
    serializer_class = GetCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data.get('phone_number')
        try:
            user = CustomUser.objects.get(phone_number=phone_number)
        except CustomUser.DoesNotExist:
            return Response({"message": _("User not found with this phone!")})
        if user.is_verified:
            return Response({"message": _("This phone number already verified!")}, status=status.HTTP_400_BAD_REQUEST)

        # send otp via message
        secret = self.send_otp(phone_number, "Your confirmation code: {code}")
        cache.set(phone_number, secret, timeout=OTP_EXPIRES_IN)

        return Response({"message": _("We have sent you a code via SMS to verify your account.")})


class VerifyCode(BaseAuthAPIView, generics.GenericAPIView):
    serializer_class = VerifyCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data.get('phone_number')
        secret = cache.get(phone_number)
        if not secret:
            return Response({"message": _("Please get code first!")}, status=status.HTTP_400_BAD_REQUEST)

        code = serializer.validated_data.get('code')
        sms_code = str(code).zfill(4)
        totp = pyotp.TOTP(secret, digits=4, interval=OTP_EXPIRES_IN)
        if totp.verify(sms_code):
            try:
                user = CustomUser.objects.get(phone_number=phone_number)
                user.is_verified = True
                user.save()
                return Response({"message": _("Your account has been verified!")})
            except CustomUser.DoesNotExist:
                return Response({"message": _("User not found with this phone!")})
        else:
            return Response({"message": _("Sms code invalid!")}, status=status.HTTP_400_BAD_REQUEST)
