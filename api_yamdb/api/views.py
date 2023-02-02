from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from reviews.models import Title, Review
from users.models import User
from .serializers import TitleSerializer, UserSerializer, ReviewSerializer

class TitleViewSet(ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = AllowAny
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter, )
    filterset_fields = ('category', 'genre', 'name', 'year')
    search_fields = ('genre', 'category')
    
    def get_review(self):
        reviews = get_object_or_404(Review, pk=self.kwargs.get('title_id'))
        return reviews


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser, )

    @action(
        detail=False,
        methods=['GET', 'PATCH'],
        permission_classes=[IsAuthenticated])
    def me(self):
        user = self.request.user
        if self.request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = self.get_serializer(user, data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.all()
