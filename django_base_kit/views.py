from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import FormView, View

from . import forms


def _get_base_kit_setting(key, default):
    """Read a key from settings.BASE_KIT with fallback to the provided default."""
    base_kit_settings = getattr(settings, "BASE_KIT", {})
    if not isinstance(base_kit_settings, dict):
        return default
    return base_kit_settings.get(key) or default


class SignUpView(FormView):
    """Handle creation of a new user via the signup form."""

    form_class = forms.SignUpForm
    template_name = _get_base_kit_setting("signup_template", "signup.html")
    success_url = _get_base_kit_setting("signup_success_url", "/")

    def form_valid(self, form):
        """Create the user and continue with the configured success flow."""
        form.save()
        return super().form_valid(form)


class LoginView(FormView):
    """Display and process the user login form."""

    form_class = forms.UserLoginForm
    template_name = _get_base_kit_setting("login_template", "login.html")
    success_url = _get_base_kit_setting("login_success_url", "/")

    def form_valid(self, form):
        """Authenticate user credentials and log in."""
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


class LogoutView(View):
    """Log the user out and redirect to the login page."""

    success_url = _get_base_kit_setting("logout_success_url", "/")

    def get(self, request):
        logout(request)
        return redirect(self.success_url)


@method_decorator(login_required(login_url="login"), name="dispatch")
class ChangePasswordView(auth_views.PasswordChangeView):
    """Allow a logged-in user to change their password."""

    template_name = _get_base_kit_setting(
        "change_password_template", "change_password.html"
    )
    success_url = "/"


class ResetPasswordView(auth_views.PasswordResetView):
    """Send password reset emails to users."""

    form_class = forms.ResetPasswordForm
    from_email = getattr(
        settings, "FROM_MAIL", getattr(settings, "DEFAULT_FROM_EMAIL", None)
    )
    html_email_template_name = _get_base_kit_setting(
        "reset_password_email_template",
        "email_templates/reset_password_email_template.html",
    )
    email_template_name = html_email_template_name
    success_url = reverse_lazy("reset-password-done")
    template_name = _get_base_kit_setting(
        "reset_password_template", "password_reset/reset_password_form.html"
    )
    title = "Recuperar senha"
    use_https = True


class ResetPasswordDoneView(auth_views.PasswordResetDoneView):
    """Simple confirmation page after password reset email sent."""

    template_name = _get_base_kit_setting(
        "reset_password_done_template", "password_reset/reset_password_done.html"
    )
    title = "Recuperaçao de senha enviada"


class ResetPasswordConfirmView(auth_views.PasswordResetConfirmView):
    """Form for entering a new password after reset link."""

    success_url = reverse_lazy("password-reset-complete")
    template_name = _get_base_kit_setting(
        "reset_password_confirm_template", "password_reset/reset_password_confirm.html"
    )


class ResetPasswordCompleteView(auth_views.PasswordResetCompleteView):
    """Final page displayed after a successful password reset."""

    template_name = _get_base_kit_setting(
        "reset_password_complete_template", "password_reset/reset_password_complete.html"
    )

    def get_context_data(self, **kwargs):
        """Insert login url into template context."""
        context = super().get_context_data(**kwargs)
        context["login_url"] = "login"
        return context
