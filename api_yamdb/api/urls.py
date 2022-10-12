from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (CategoryViewSet, GenreViewSet, TitleViewSet,
                    ReviewViewSet, CommentViewSet)

router = SimpleRouter()
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
router.register('titles', TitleViewSet)

review_router = SimpleRouter()
review_router.register('reviews', ReviewViewSet)

comment_router = SimpleRouter()
comment_router.register('comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('titles/<int:title_id>/', include(review_router.urls)),
    path('titles/<int:title_id>/reviews/<int:review_id>/',
         include(comment_router.urls)),
    # path('auth/', ),  todo: add auth urls
    # path('users/', ),  todo: add users urls
    # path('users/<slug:username>', ),  todo: add user urls
]