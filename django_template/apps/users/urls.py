from django.urls import path
from .views import UserSettingsDetail

urlpatterns = [
    path('api/user-settings/', UserSettingsDetail.as_view(), name='user-settings-detail'),
]