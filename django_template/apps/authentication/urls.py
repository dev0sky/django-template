from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from authentication.views import LogoutView, RegisterUser, LoginView, CustomTokenValidationView

app_name = 'authentication'

urlpatterns = [
     path('api/login/', LoginView.as_view(), name='api_login'),
     path('api/logout/', LogoutView.as_view(), name='api_logout'),
     path('api/register/', RegisterUser.as_view(), name='api_register'),
     path('api/token/', jwt_views.TokenObtainPairView.as_view(), name ='api_token'),
     path('api/token_refresh/', jwt_views.TokenRefreshView.as_view(), name ='api_token_refresh'),
     path('api/token_validation/', CustomTokenValidationView.as_view(), name='api_token_validation'),
]