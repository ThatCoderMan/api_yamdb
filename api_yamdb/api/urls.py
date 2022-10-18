from django.urls import include, path
from rest_framework.routers import SimpleRouter

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
    path('v1/', include(router.urls)),
    path('v1/titles/<int:title_id>/', include(review_router.urls)),
    path('v1/titles/<int:title_id>/reviews/<int:review_id>/',
         include(comment_router.urls)),
]
