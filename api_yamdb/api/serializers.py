from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.relations import SlugRelatedField
from reviews.models import Comment, Review, Title


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'text', 'score', 'author', 'pub_date')
        model = Review

    def validate(self, attrs):
        title_id = self.context['title_id']
        user = self.context['request'].user
        method = self.context['request'].method
        title = get_object_or_404(Title, pk=title_id)
        if (method == 'POST'
                and Review.objects.filter(title=title, author=user).exists()):
            raise ValidationError()
        return attrs


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
