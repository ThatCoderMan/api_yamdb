from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from reviews.models import Comment, Review, Title

from .permissions import (IsAdminOrReadOnly, IsAuthorOrReadOnly,
                          IsModeratorOrReadOnly)
from .review_serializers import CommentSerializer, ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly
                          | IsModeratorOrReadOnly | IsAuthorOrReadOnly)

    def get_queryset(self):
        title_id = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return Review.objects.filter(title=title_id)

    def perform_create(self, serializer):
        serializer.save(
            title=get_object_or_404(
                Title, pk=self.kwargs['title_id'], ),
            author=self.request.user,
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['title_id'] = self.kwargs.get('title_id')
        context['request'] = self.request
        return context


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly
                          | IsModeratorOrReadOnly | IsAuthorOrReadOnly)

    def get_queryset(self):
        review_id = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return Comment.objects.filter(review=review_id)

    def perform_create(self, serializer):
        serializer.save(
            review=get_object_or_404(
                Review, pk=self.kwargs['review_id'], ),
            author=self.request.user,
        )
