from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken
from .models import CustomUser


class CustomUserJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION")

        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        raw_token = auth_header.split(" ")[1]

        try:
            token = AccessToken(raw_token)
        except Exception:
            raise AuthenticationFailed("Invalid or expired token")

        user_id = token.get("user_id")

        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            raise AuthenticationFailed("User not found")

        user.is_authenticated = True
        return (user, token)