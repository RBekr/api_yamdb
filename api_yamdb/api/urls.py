from django.urls import include, path
from rest_framework import routers

from .views import CommentViewSet, ReviewViewSet, TitleViewSet, UserViewSet

router_v1 = routers.DefaultRouter()
router_v1.register('v1/users', UserViewSet, basename='users')
router_v1.register('v1/titles', TitleViewSet, basename='titles')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='review'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comment',
)

urlpatterns = [
    path('', include(router_v1.urls))
]
