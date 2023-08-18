from django.contrib import admin

from users.models import CustomUser, InviteCode


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ["id", "phone_number", "invite_code"]


@admin.register(InviteCode)
class InviteCodeAdmin(admin.ModelAdmin):
    list_display = ["id", "code", "created_at", "updated_at"]
