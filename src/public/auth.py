from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from django.contrib import messages

class EmailBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        UserModel = get_user_model()

        # print(kwargs)

        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                if not user.is_active:
                    if 'request' in kwargs:
                        messages.warning(kwargs['request'],
                                         'Seu usuário está desativado, contate a equipe de administração')
                    else:
                        print('HandmadeWarning: this user is not active')

                    return None
                return user
        return None
