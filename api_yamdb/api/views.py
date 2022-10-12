from rest_framework import viewsets
from rest_framework.mixins import (CreateModelMixin,
                                   ListModelMixin,
                                   DestroyModelMixin)

from reviews.models import Category, Genre, Title, Review, Comment


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
    http_method_names = ['get', 'post', 'patch', 'del']  # we don't use put


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    http_method_names = ['get', 'post', 'patch', 'del']  # we don't use put


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    http_method_names = ['get', 'post', 'patch', 'del']  # we don't use put
