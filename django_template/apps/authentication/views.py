from rest_framework import status
from django.contrib.auth import login
from rest_framework.views import APIView
from rest_framework.response import Response
from users.serializers import UserSerializer
from django.utils.translation import gettext_lazy as _ 
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from django.contrib.auth import authenticate, get_user_model 
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import TokenError, AccessToken

import logging

logger = logging.getLogger(__name__)

User = get_user_model()

class RegisterUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        logger.info(f"Received registration data: {request.data}")

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': _('User created successfully')}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                refresh = RefreshToken.for_user(user)
                access_token = refresh.access_token
                
                # Serializar el usuario con la información extendida
                user_data = UserSerializer(user).data 
                print(user_data)

                return Response({
                    'refresh': str(refresh),
                    'access': str(access_token),
                    'user': user_data,  # Incluir los datos serializados del usuario
                    'expiresIn': access_token.lifetime.total_seconds(),  # Expiración en segundos
                    'refreshExpiresIn': refresh.lifetime.total_seconds()  # Expiración en segundos
                })
            else:
                return Response({'detail': 'User account is disabled'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": _('Logged out successfully')}, status=status.HTTP_205_RESET_CONTENT)
        except TokenError:
            return Response({"error": "Token de actualización inválido"}, status=status.HTTP_400_BAD_REQUEST)
 
class CustomTokenValidationView(APIView):
    def post(self, request):
        access_token = request.data.get('access')
        if not access_token:
            return Response({'error': _('An access token was not provided')}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = AccessToken(access_token)
            token.verify()
            print(f'Token valido por {token.lifetime.total_seconds()} segundos	')
            return Response({'detail': _('Valid access token')}, status=status.HTTP_200_OK)
        except TokenError:
            print('Token invalido')
            return Response({'error': _('Invalid access token')}, status=status.HTTP_401_UNAUTHORIZED)
        
class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            print(response.data)
            return response
        except TokenError as e:
            print(e)
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
