from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


class UserAdmin(BaseUserAdmin):
    list_display = (
        "email",
        "username",
        "first_name",
        "last_name",
        "is_admin",
    )
    list_filter = ("is_admin",)
    fieldsets = (
        (None, {"fields": ("username", "first_name", "last_name", "password")}),
        ("Email", {"fields": ("email",)}),
        (
            "Personal info",
            {"fields": ("avatar",)},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_admin",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                    "is_admin",
                ),
            },
        ),
    )
    search_fields = (
        "email",
        "username",
        "first_name",
        "last_name",
    )


admin.site.register(User, UserAdmin)
