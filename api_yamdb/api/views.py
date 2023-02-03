from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from reviews.models import Category, Genre, Review, Title
from users.models import User

from .serializers import (CategorySerializer, GenreSerializer,
                          ReviewSerializer, TitleSerializerMany,
                          TitleSerializerOne, UserSerializer)


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.select_related('category').\
        prefetch_related('genre')
    serializer_class_one = TitleSerializerOne
    serializer_class_many = TitleSerializerMany

    permission_classes = [AllowAny,]
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'name', 'year')

    
    def get_serializer_class(self):
        if self.action in ['list','retrieve']:
            return TitleSerializerMany
        return TitleSerializerOne 


    def get_review(self):
        reviews = get_object_or_404(Review, pk=self.kwargs.get('title_id'))
        return reviews


class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    permission_classes = [AllowAny,]
    search_field = ('name',)
    lookup_field = 'slug'


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    permission_classes = [AllowAny,]
    search_field = ('name',)
    lookup_field = 'slug'


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
