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
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Comment, Genre, Review, Title, User

from .filters import TitleFilter
from .permissions import IsAdmin, IsAdminOrModeratorOrMe, IsAdminOrReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, SignUpSerialiser,
                          TitleEditSerializer, TitleGetSerializer,
                          TokenSerializer, UserSerializer)


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
            user = get_object_or_404(User,
                                     username=serializer.data['username'])
            if user.confirmation_code == serializer.data['confirmation_code']:
                return Response(
                    {'token': str(RefreshToken.for_user(user).access_token)},
                    status=status.HTTP_200_OK
                )
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


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdmin)
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    # todo: users/me
    #  Прописать get_queryset и get_permissions для работы со своим аккаунтом


class CategoryViewSet(CreateListDestroyModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(CreateListDestroyModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('review__score'))
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (IsAdminOrReadOnly,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleGetSerializer
        return TitleEditSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrModeratorOrMe,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
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
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrModeratorOrMe,)

    http_method_names = ['get', 'post', 'patch', 'delete']
    serializer_class = CommentSerializer

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        return Comment.objects.filter(review=review_id)

    def perform_create(self, serializer):
        serializer.save(
            review=get_object_or_404(
                Review, pk=self.kwargs['review_id'], ),
            author=self.request.user,
        )
