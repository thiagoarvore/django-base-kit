from django.shortcuts import render
from django.urls import path

from . import views


def first_login_view(request):
    return render(request, "firstlogin.html", {})


user_urlpatterns = [
    path("accounts/signup/", views.SignUpView.as_view(), name="signup"),
    path("accounts/login/", views.LoginView.as_view(), name="login"),
    path("accounts/logout/", views.LogoutView.as_view(), name="logout"),
    path(
        "change_password/", views.ChangePasswordView.as_view(), name="change_password"
    ),
    path("reset_password/", views.ResetPasswordView.as_view(), name="password-reset"),
    path(
        "reset_password/done",
        views.ResetPasswordDoneView.as_view(),
        name="reset-password-done",
    ),
    path(
        "reset_password/confirm/<uidb64>/<token>/",
        views.ResetPasswordConfirmView.as_view(),
        name="password-reset-confirm",
    ),
    path(
        "reset_password/complete/",
        views.ResetPasswordCompleteView.as_view(),
        name="password-reset-complete",
    ),
    # path("user_detail/<str:pk>", views.UserDetailView.as_view(), name="user_detail"),
    # path(
    #     "user_detail/<str:pk>/edit",
    #     views.UserUpdateView.as_view(),
    #     name="edit_user_detail",
    # ),
    # path('delete_user/', views.delete_account, name='delete_user'),
]
