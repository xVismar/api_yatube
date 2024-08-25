from django.utils import timezone
from rest_framework import serializers

from posts.models import Comment, Group, Post


class AuthorMixin(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'


class PostSerializer(AuthorMixin):

    class Meta:
        model = Post
        fields = '__all__'


class CommentSerializer(AuthorMixin):
    created = serializers.DateTimeField(
        default=serializers.CreateOnlyDefault(timezone.now),
        read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('post',)
