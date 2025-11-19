from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class EmailOrUsernameTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # ajoute infos utiles au payload si besoin
        token["username"] = user.username
        token["email"] = user.email
        return token

    def validate(self, attrs):
        # attrs contient 'username' et 'password' par défaut ; on accepte 'email' aussi
        username = attrs.get("username")
        password = attrs.get("password")

        # si email fourni dans username param
        try:
            user_obj = None
            if username and "@" in username:
                user_obj = User.objects.filter(email__iexact=username).first()
                if user_obj:
                    username = user_obj.username
                    attrs["username"] = username
        except Exception:
            pass

        data = super().validate(attrs)
        return data
