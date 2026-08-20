from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

UserModel = get_user_model()

class PlainTextModelBackend(ModelBackend):
    """
    Custom authentication backend that supports:
    - Plain-text password authentication
    - Fallback to Django check_password for legacy hashes
    - Logging in with EITHER Username OR Email (case-insensitive)
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD) or kwargs.get('email')
        if username is None or password is None:
            return None

        username = str(username).strip()

        # Find user by username OR email (case-insensitive)
        user = UserModel.objects.filter(
            Q(username__iexact=username) | Q(email__iexact=username)
        ).first()

        if user is None:
            return None

        # Check plain-text password match or hashed password match
        if (user.password == password or user.check_password(password)) and self.user_can_authenticate(user):
            return user

        return None
