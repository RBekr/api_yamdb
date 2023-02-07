from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User

from .permissions import IsAdmin, IsAuthorAdminModeratorOrReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleSerializerMany, TitleSerializerOne,
                          TokenSerializer, UserSerializer,
                          UserSignUpSerializer)


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.select_related('category').\
        prefetch_related('genre')
    serializer_class_one = TitleSerializerOne
    serializer_class_many = TitleSerializerMany

    permission_classes = [AllowAny, ]  # изменить в след. фиче IsAdminUser
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'name', 'year')

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitleSerializerMany
        return TitleSerializerOne

    def get_review(self):
        reviews = get_object_or_404(Review, pk=self.kwargs.get('title_id'))
        return reviews


class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    permission_classes = [AllowAny, ]  # изменить в след. фиче IsAdminUser
    search_field = ('name',)
    lookup_field = 'slug'


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    permission_classes = [AllowAny, ]  # изменить в след. фиче IsAdminUser
    search_field = ('name',)
    lookup_field = 'slug'


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin, )
    filter_backends = (filters.SearchFilter, )
    lookup_field = 'username'
    search_fields = ('username',)

    @action(
        detail=False,
        methods=['GET', 'PATCH'],
        permission_classes=[IsAuthenticated])
    def me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = self.get_serializer(
            user,
            data=self.request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserSignUpAPI(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):

        serializer = UserSignUpSerializer(
            data=request.data
        )
        if serializer.is_valid():
            user, b = User.objects.get_or_create(
                **serializer.validated_data
            )
            confirmation_code = default_token_generator.make_token(user)
            send_mail(
                subject='Код подтверждения для регистрации',
                message=f'Дорогой, {user.username}, для регистрации на yamdb. '
                        f'Cкопируйте код подтверждения {confirmation_code}',
                from_email='yamdb@yamdb.com',
                recipient_list=[f'{user.email}'],
                fail_silently=False
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenAPI(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        confirmation_code = serializer.validated_data.get(
            'confirmation_code'
        )
        user = get_object_or_404(User, username=username)
        if default_token_generator.check_token(user, confirmation_code):
            token = AccessToken.for_user(user)
            return Response(
                {'token': str(token)}, status=status.HTTP_200_OK
            )
        return Response(
            {'confirmation_code': 'Неверный код подтверждения!'},
            status=status.HTTP_400_BAD_REQUEST
        )


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAuthorAdminModeratorOrReadOnly,)

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.all()


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAuthorAdminModeratorOrReadOnly,)

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(title.reviews, id=review_id)
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(title.reviews, id=review_id)
        return review.comments.all()
