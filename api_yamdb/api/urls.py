from django.urls import include, path
from rest_framework import routers

from .views import UserViewSet

router_v1 = routers.DefaultRouter()
router_v1.register('v1/users', UserViewSet, basename='users')
router_v1.register('v1/titles', TitleViewSet, basename='titles')

urlpatterns = [
    path('', include(router_v1.urls))
]