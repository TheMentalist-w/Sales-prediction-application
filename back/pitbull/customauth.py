from django.contrib.auth import  get_user_model, backends

class CustomAuthBackend(backends.ModelBackend):
    def authenticate(self, request, username=None, password=None):
        if '@' in username:
            user_arg = {'email' : username }
        else: 
            user_arg = {'username' : username }
        try:
            user_res = get_user_model().objects.get(**user_arg)
            if user_res.check_password(password):
                return user_res
        except get_user_model().DoesNotExist:
            return None