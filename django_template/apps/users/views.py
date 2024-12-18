from .models import UserSettings
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from users.serializers import UserSerializer
from django.shortcuts import get_object_or_404
from .serializers import UserSettingsSerializer
from rest_framework import generics, permissions
from persons.serializers import PersonSerializer
from rest_framework.permissions import IsAuthenticated
from social.serializers import CommonProfileSerializer

class UserSettingsDetail(generics.RetrieveUpdateAPIView):
    queryset = UserSettings.objects.all()
    serializer_class = UserSettingsSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return UserSettings.objects.get(user=self.request.user)
        except UserSettings.DoesNotExist:
            # Handle the case when UserSettings does not exist
            # You can either raise a 404 error or create a default UserSettings object
            # Here's an example of raising a 404 error
            raise get_object_or_404(UserSettings, user=self.request.user)
        

class UserUpdateView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()

        # Actualiza UserSettings
        settings_data = request.data.get('settings')
        if settings_data:
            settings_serializer = UserSettingsSerializer(user.usersettings, data=settings_data, partial=True)
            if settings_serializer.is_valid():
                settings_serializer.save()
            else:
                return Response(settings_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Actualiza CommonProfile
        profile_data = request.data.get('profile')
        if profile_data:
            common_profile_serializer = CommonProfileSerializer(user.commonprofile, data=profile_data, partial=True)
            if common_profile_serializer.is_valid():
                common_profile_serializer.save()

                # Actualiza Person si está incluido
                person_data = profile_data.get('person')
                if person_data and user.commonprofile.person:
                    person_serializer = PersonSerializer(user.commonprofile.person, data=person_data, partial=True)
                    if person_serializer.is_valid():
                        person_serializer.save()
                    else:
                        return Response(person_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response(common_profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Si todo es válido, guarda y retorna la respuesta
        user_serializer = UserSerializer(user)
        return Response(user_serializer.data)
