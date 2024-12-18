from social.models import Post
from core.views import UserCachedListViewSet
from rest_framework import permissions
from social.serializers import PostSerializer

app_name = 'social'

class PostViewSet(UserCachedListViewSet):
    queryset = Post.objects.filter(is_active=True).order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated] 
    app_name = app_name
    model_name = 'post'
