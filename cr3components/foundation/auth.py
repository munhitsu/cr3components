from django.contrib.auth.models import User
from django.contrib.sites.models import Site


class EmailAuth(object):
    """
    authenticate against user email
    """
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def authenticate(self, username=None, password=None):
        try:
            print "auth (%s, %s)" % (username, password)
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
