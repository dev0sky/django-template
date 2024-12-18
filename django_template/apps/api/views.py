from users.models import User
from rest_framework import viewsets
from api.serializers import  UserSerializer

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
