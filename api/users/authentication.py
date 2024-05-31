from typing import Optional, Tuple, TypeVar

from django.contrib.auth import get_user_model
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.models import TokenUser
from rest_framework_simplejwt.tokens import Token

from users.models import User

AuthUser = TypeVar("AuthUser", User, TokenUser)


class MyJWTAuthentication(JWTAuthentication):
    """
    An authentication plugin that authenticates requests through a JSON web
    token provided in a request header.
    """

    www_authenticate_realm = "api"
    media_type = "application/json"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.user_model = get_user_model()

    def authenticate(self, request: Request) -> Optional[Tuple[AuthUser, Token]]:
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)

        return self.get_user(validated_token), validated_token


    # def get_user(self, validated_token: Token) -> AuthUser:
    #     """
    #     Attempts to find and return a user using the given validated token.
    #     """
    #     try:
    #         user_id = validated_token[api_settings.USER_ID_CLAIM]
    #     except KeyError:
    #         raise InvalidToken(_("Token contained no recognizable user identification"))
    #
    #     try:
    #         user = self.user_model.objects.get(**{api_settings.USER_ID_FIELD: user_id})
    #     except self.user_model.DoesNotExist:
    #         raise AuthenticationFailed(_("User not found"), code="user_not_found")
    #
    #     if not user.is_active:
    #         raise AuthenticationFailed(_("User is inactive"), code="user_inactive")
    #
    #     if api_settings.CHECK_REVOKE_TOKEN:
    #         if validated_token.get(
    #             api_settings.REVOKE_TOKEN_CLAIM
    #         ) != get_md5_hash_password(user.password):
    #             raise AuthenticationFailed(
    #                 _("The user's password has been changed."), code="password_changed"
    #             )
    #
    #     return user


def default_user_authentication_rule(user: AuthUser) -> bool:
    # Prior to Django 1.10, inactive users could be authenticated with the
    # default `ModelBackend`.  As of Django 1.10, the `ModelBackend`
    # prevents inactive users from authenticating.  App designers can still
    # allow inactive users to authenticate by opting for the new
    # `AllowAllUsersModelBackend`.  However, we explicitly prevent inactive
    # users from authenticating to enforce a reasonable policy and provide
    # sensible backwards compatibility with older Django versions.
    return user is not None and user.is_active