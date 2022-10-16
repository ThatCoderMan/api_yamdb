from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet, UserViewSet,
                    ReviewViewSet, SignUpView, TitleViewSet, TokenView)

router = SimpleRouter()
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
router.register('titles', TitleViewSet)

review_router = SimpleRouter()
review_router.register('reviews', ReviewViewSet, basename='reviews')

comment_router = SimpleRouter()
comment_router.register('comments', CommentViewSet, basename='comments')

user_router = SimpleRouter()
user_router.register('', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('titles/<int:title_id>/', include(review_router.urls)),
    path('titles/<int:title_id>/reviews/<int:review_id>/',
         include(comment_router.urls)),
    path('users/', include(user_router.urls)),
    path('auth/signup/', SignUpView.as_view()),
    path('auth/token/', TokenView.as_view())
]
