from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .auth_views import SignUpView, TokenView, UserViewSet
from .review_views import CommentViewSet, ReviewViewSet
from .title_views import CategoryViewSet, GenreViewSet, TitleViewSet

router = SimpleRouter()
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
router.register('titles', TitleViewSet)
router.register('users', UserViewSet)

review_router = SimpleRouter()
review_router.register('reviews', ReviewViewSet, basename='reviews')

comment_router = SimpleRouter()
comment_router.register('comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/titles/<int:title_id>/', include(review_router.urls)),
    path('v1/titles/<int:title_id>/reviews/<int:review_id>/',
         include(comment_router.urls)),
    path('v1/auth/signup/', SignUpView.as_view()),
    path('v1/auth/token/', TokenView.as_view())
]
