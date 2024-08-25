from rest_framework import serializers
from django.utils import timezone

from posts.models import Comment, Group, Post


class AuthorMixin(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')
        read_only_fields = ('id',)


class PostSerializer(AuthorMixin):

    class Meta:
        model = Post
        fields = ('id', 'text', 'pub_date', 'author', 'image', 'group')
        read_only_fields = ('id',)


class CommentSerializer(AuthorMixin):
    created = serializers.DateTimeField(
        default=serializers.CreateOnlyDefault(timezone.now),
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created')
        read_only_fields = ('id', 'post',)
