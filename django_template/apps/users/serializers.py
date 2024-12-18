import re
from rest_framework import serializers
from .models import User, UserSettings
from social.models import CommonProfile
from django.contrib.auth import get_user_model
from allauth.account.models import EmailAddress
from django.utils.translation import gettext_lazy as _
from social.serializers import CommonProfileSerializer


User = get_user_model()

class UserSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSettings
        fields = '__all__'
 
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    settings = UserSettingsSerializer(source='usersettings_fk_user', read_only=True)
    profile = CommonProfileSerializer(source='commonprofile_fk_user', read_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role', 'settings', 'profile']

    def validate_password(self, value):
        password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$'
        if not re.match(password_regex, value):
            raise serializers.ValidationError(_('Password must contain at least 8 characters, one uppercase letter, one lowercase letter, and one number.'))
        return value

    def validate_role(self, value):
        if value not in ['client', 'contributor']:
            raise serializers.ValidationError(_('Invalid role'))
        return value

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            role=validated_data['role']
        )
        user.set_password(validated_data['password'])
        user.save()

        # Crear instancias de UserSettings y CommonProfile
        UserSettings.objects.get_or_create(user=user)
        CommonProfile.objects.get_or_create(user=user, name='default', description='Auto-generated profile')

        # Añadir el correo electrónico a la tabla account_emailaddress
        EmailAddress.objects.create(
            user=user,
            email=validated_data['email'],
            verified=False,  # Puedes cambiar esto según tu lógica de verificación de email
            primary=True
        )
        return user
