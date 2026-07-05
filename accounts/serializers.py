from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError('No active account found with the given credentials')

        # Authenticate using the real username behind the scenes
        user = authenticate(username=user_obj.username, password=password)
        if user is None:
            raise serializers.ValidationError('No active account found with the given credentials')

        # Manually build the token pair instead of relying on parent's validate()
        refresh = self.get_token(user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return data