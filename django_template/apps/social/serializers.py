from rest_framework import serializers
from social.models import Post, Comment, Profile, CommonProfile
from persons.serializers import PersonNoSensibleInformationSerializer

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'

class CommonProfileSerializer(serializers.ModelSerializer):
    person = PersonNoSensibleInformationSerializer(read_only=True, required=False)  # `required=False` para manejar `null`
    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()
    # posts = PostSerializer(source='post_fk_profile', many=True, read_only=True)

    class Meta:
        model = CommonProfile
        fields = ['name', 'description', 'is_active', 'type', 'created_at', 'updated_at', 'person', 'followers', 'following']

    def get_followers(self, obj):
        return obj.followers.count()

    def get_following(self, obj):
        return obj.following.count()

class PostSerializer(serializers.ModelSerializer):
    author = CommonProfileSerializer(source='post_fk_author', read_only=True, required=False)  # `required=False` para manejar `null`

    class Meta:
        model = Post
        fields = '__all__'