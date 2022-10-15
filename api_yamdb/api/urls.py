from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .cauth_views import SignUpViewSet
from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet)

router = SimpleRouter()
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
router.register('titles', TitleViewSet)

review_router = SimpleRouter()
review_router.register('reviews', ReviewViewSet, basename='reviews')

comment_router = SimpleRouter()
comment_router.register('comments', CommentViewSet, basename='comments')


urlpatterns = [
    path('', include(router.urls)),
    path('titles/<int:title_id>/', include(review_router.urls)),
    path('titles/<int:title_id>/reviews/<int:review_id>/',
         include(comment_router.urls)),
    path('auth/signup/', SignUpViewSet.as_view()),  # todo: add auth urls
    # path('users/', ),  todo: add users urls
    # path('users/<slug:username>', ),  todo: add user urls
]