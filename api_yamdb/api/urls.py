from django.urls import include, path

from .routers import NoPutRouter
from .views import TitleViewSet, TokenAPI, UserSignUpAPI, UserViewSet

router_v1 = NoPutRouter()
router_v1.register('v1/users', UserViewSet, basename='users')
router_v1.register('v1/titles', TitleViewSet, basename='titles')

urlpatterns = [
    path('', include(router_v1.urls)),
    path('v1/auth/signup/', UserSignUpAPI.as_view(), name='signup'),
    path('v1/auth/token/', TokenAPI.as_view(), name='tokens'),
]
