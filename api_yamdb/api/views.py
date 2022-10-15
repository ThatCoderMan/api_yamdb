from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Comment, Genre, Review, Title, User

from .filters import TitleFilter
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, SignUpSerialiser,
                          TitleSerializer, TokenSerializer)


def send_email_confirmation(user, confirmation_code):
    subject = f'Confirmation of user registration for "{user}"'
    message = (
        'Use the confirmation code to get the token.\n'
        f'Confirmation code: {confirmation_code}'
    )
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email, ])


class CreateListDestroyModelViewSet(CreateModelMixin,
                                    ListModelMixin,
                                    DestroyModelMixin,
                                    viewsets.GenericViewSet):
    pass


class TokenView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                user = get_object_or_404(User, **serializer.data)
                return Response(
                    {'token': str(RefreshToken.for_user(user).access_token)},
                    status=status.HTTP_200_OK
                )
            except Exception as e:
                print(e)
                return Response(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignUpView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignUpSerialiser(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = User.objects.get(username=serializer.data['username'])
            if not user.confirmation_code:
                confirmation_code = default_token_generator.make_token(user)
                user.confirmation_code = confirmation_code
                user.save()
            else:
                confirmation_code = user.confirmation_code
            send_email_confirmation(user, confirmation_code)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class CategoryViewSet(CreateListDestroyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(CreateListDestroyModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('review__score'))
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    http_method_names = ['get', 'post', 'patch', 'delete']


class ReviewViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    serializer_class = ReviewSerializer

    # permission_classes = (IsTrustedOrReadOnly,)
    # здесь будет пермишн от Игоря

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        return Review.objects.filter(title_id=title_id)

    def perform_create(self, serializer):
        serializer.save(
            title_id=get_object_or_404(
                Title, pk=self.kwargs['title_id'], ),
            author=self.request.user,
        )


class CommentViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    serializer_class = CommentSerializer

    # permission_classes = (IsTrustedOrReadOnly,)
    # здесь будет пермишн от Игоря

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        return Comment.objects.filter(review_id=review_id)

    def perform_create(self, serializer):
        serializer.save(
            review_id=get_object_or_404(
                Title, pk=self.kwargs['title_id'], ),
            author=self.request.user,
        )
