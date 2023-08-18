from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from .managers import CustomUserManager
from .utils import generate_password


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CustomUser(BaseModel, AbstractUser):
    username = None
    phone_number = PhoneNumberField(_("Phone number"), unique=True)
    is_verified = models.BooleanField(_("Verified"), default=False)
    invite_code = models.ForeignKey("InviteCode", verbose_name=_("Invite Code"), on_delete=models.SET_NULL, null=True,
                                    blank=True)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self) -> str:
        return f"<User ID: {self.id} Phone: {self.phone_number}>"

    def save(self, *args, **kwargs):
        if not self.password:
            self.set_password(generate_password())
        super().save(*args, **kwargs)


class InviteCode(BaseModel):
    code = models.CharField(max_length=6, default=generate_password())
