"""Admin configuration for the accounts app."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class CustomUserAdmin(UserAdmin):
    """Admin interface options for the custom User model."""

    model = User
    list_display = (
        "username",
        "active",
        "email",
        "first_name",
        "last_name",
        "is_staff",
    )
    list_filter = ("is_staff","active")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("first_name",)

    # Campos exibidos ao editar um usuário
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Informações pessoais", {"fields": ("first_name", "last_name")}),
        (
            "Permissões",
            {
                "fields": (
                    "username",
                    "active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Datas importantes", {"fields": ("last_login", "date_joined")}),
    )

    # Campos exibidos ao adicionar um novo usuário
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                    "is_staff",
                    "active",
                ),
            },
        ),
    )


# Registrar o usuário com a nova classe CustomUserAdmin
admin.site.register(User, CustomUserAdmin)
