from api import views
from django.urls import path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# USERS
router.register(r'users', views.UserViewSet, basename='users')

urlpatterns = router.urls
urlpatterns += [
]