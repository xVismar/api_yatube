from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from api.permissions import IsAuthor
from api.serializers import CommentSerializer, GroupSerializer, PostSerializer
from posts.models import Group, Post


class ViewSetBase(viewsets.ModelViewSet):
    """Базовый класс-родитель для указания разрешений и класса viewset."""

    permission_classes = (IsAuthor,)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для просмотра групп.

    Предоставляет только операции GET, HEAD, OPTIONS для модели Group.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PostViewSet(ViewSetBase):
    """ViewSet для управления постами.

    Позволяет выполнять CRUD операции для модели Post.
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        """Устанавливает текущего пользователя как автора поста."""
        serializer.save(author=self.request.user)


class CommentViewSet(ViewSetBase):
    """ViewSet для управления комментариями.

    Позволяет выполнять CRUD операции для модели Comment.
    """

    serializer_class = CommentSerializer

    def get_post(self):
        """Получает пост по post_id из URL, возвращает 404 если не найден."""
        return get_object_or_404(Post, pk=self.kwargs.get('post_id'))

    def get_queryset(self):
        """Возвращает QuerySet с комментариями для конкретного поста."""
        return self.get_post().comments.all()

    def perform_create(self, serializer):
        """Переопределение метода создания комментария.

        Устанавливает текущего пользователя как автора комментария и связывает
        комментарий с постом.
        """
        serializer.save(author=self.request.user, post=self.get_post())
