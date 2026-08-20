from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

UserModel = get_user_model()

class PlainTextModelBackend(ModelBackend):
    """
    Custom authentication backend that supports:
    - Plain-text password authentication
    - Fallback to Django check_password for legacy hashes
    - Logging in with EITHER Username OR Email (case-insensitive, whitespace-tolerant)
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD) or kwargs.get('email')
        if username is None or password is None:
            return None

        username = str(username).strip()
        pwd = str(password)
        pwd_strip = pwd.strip()

        # Find user by username OR email (case-insensitive)
        user = UserModel.objects.filter(
            Q(username__iexact=username) | Q(email__iexact=username)
        ).first()

        if user is None:
            return None

        # Check plain-text password match (exact and trimmed) or check_password
        plain_match = (
            user.password == pwd or
            user.password == pwd_strip or
            user.password.strip() == pwd_strip
        )

        hash_match = False
        try:
            hash_match = user.check_password(pwd) or user.check_password(pwd_strip)
        except Exception:
            hash_match = False

        if (plain_match or hash_match) and self.user_can_authenticate(user):
            return user

        return None

