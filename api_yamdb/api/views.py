from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)

from reviews.models import Category, Comment, Genre, Review, Title
from .serializers import CommentSerializer, ReviewSerializer


class CreateListDestroyModelViewSet(CreateModelMixin,
                                    ListModelMixin,
                                    DestroyModelMixin,
                                    viewsets.GenericViewSet):
    pass


class CategoryViewSet(CreateListDestroyModelViewSet):
    queryset = Category.objects.all()


class GenreViewSet(CreateListDestroyModelViewSet):
    queryset = Genre.objects.all()


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']  # we don't use put


class ReviewViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']  # we don't use put
    serializer_class = ReviewSerializer
    # permission_classes = (IsTrustedOrReadOnly,)
    # здесь будет пермишн от Игоря

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        return Review.objects.filter(title_id=title_id)

    def perform_create(self, serializer):
        serializer.save(
            title_id=get_object_or_404(
                Title, pk=self.kwargs['title_id'],),
            author=self.request.user,
        )


class CommentViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']  # we don't use put
    serializer_class = CommentSerializer
    # permission_classes = (IsTrustedOrReadOnly,)
    # здесь будет пермишн от Игоря

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        return Comment.objects.filter(review_id=review_id)

    def perform_create(self, serializer):
        serializer.save(
            review_id=get_object_or_404(
                Title, pk=self.kwargs['title_id'],),
            author=self.request.user,
        )
