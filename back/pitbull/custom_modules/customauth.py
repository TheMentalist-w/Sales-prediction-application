from django.contrib.auth import  get_user_model, backends
from django.db.models import Q


class CustomAuthBackend(backends.ModelBackend):
    def authenticate(self, request, username=None, email=None,password=None):
            try:
                user_res = get_user_model().objects.get(Q(username=username) | Q(email=email))
                if user_res.check_password(password):
                    return user_res
            except get_user_model().DoesNotExist:
                return None