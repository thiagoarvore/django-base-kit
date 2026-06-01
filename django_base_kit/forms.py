"""Forms for managing user accounts."""

from .models import User
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    UserChangeForm as DjangoUserChangeForm,
    UserCreationForm,
)
from django.utils.translation import gettext_lazy as _


class SignUpForm(UserCreationForm):
    """Form used for registering new users."""

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        """Customize field labels and error messages."""
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Nome de usuário"
        self.fields["email"].label = "Endereço de e-mail"
        self.fields["password1"].label = "Senha"
        self.fields["password2"].label = "Confirmação de senha"
        self.fields["username"].error_messages.update(
            {
                "required": _("Este campo é obrigatório."),
                "unique": _("Este nome de usuário já está em uso."),
                "invalid": _(
                    "O nome de usuário não deve conter espaços, deve conter apenas letras, números e @/./+/-/_ caracteres."
                ),
            }
        )
        self.fields["email"].error_messages.update(
            {
                "required": _("Este campo é obrigatório."),
                "invalid": _("Insira um endereço de e-mail válido."),
            }
        )
        self.fields["password1"].error_messages.update(
            {
                "required": _("Este campo é obrigatório."),
                "password_too_short": _("A senha é muito curta."),
                "password_too_common": _("Esta senha é muito comum."),
                "password_entirely_numeric": _(
                    "A senha não pode ser completamente numérica."
                ),
            }
        )
        self.fields["password2"].error_messages.update(
            {
                "required": _("Este campo é obrigatório."),
                "password_mismatch": _("As senhas não coincidem."),
            }
        )
        self.help_texts = {
            "username": _(
                "Este será seu nome de usuário único, e será apenas utilizado para login."
            ),
            "password1": _(""),
            "password2": _("Digite a mesma senha novamente para verificação."),
        }


class UserLoginForm(AuthenticationForm):
    """Form used for user authentication."""

    def __init__(self, *args, **kwargs):
        """Set Portuguese labels for login fields."""
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Nome de usuário"
        self.fields["password"].label = "Senha"


class ChangePasswordForm(PasswordChangeForm):
    """Form used to allow users to change their password."""

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        """Customize error messages for password validation."""
        super().__init__(*args, **kwargs)
        self.error_messages["password_mismatch"] = _("As senhas não coincidem.")
        self.error_messages["password_too_common"] = _("Esta senha é muito comum.")
        self.error_messages["password_entirely_numeric"] = _(
            "A senha não pode ser completamente numérica."
        )


class ResetPasswordForm(PasswordResetForm):
    """Form used for requesting a password reset email."""

    class Meta:
        model = User
        fields = ["email"]

        labels = {"email": "Endereço de e-mail"}

    def __init__(self, *args, **kwargs):
        """Apply custom labels to reset password form."""
        super().__init__(*args, **kwargs)
        self.fields["email"].label = "Endereço de e-mail"


class UserChangeForm(DjangoUserChangeForm):
    """Form used by users to update profile information."""

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name"]

    def __init__(self, *args, **kwargs):
        """Hide the password field when editing a user."""
        super().__init__(*args, **kwargs)
        if "password" in self.fields:
            self.fields.pop("password")
