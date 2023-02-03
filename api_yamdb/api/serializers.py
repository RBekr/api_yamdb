import django.utils.timezone as timezone

from rest_framework import serializers
from reviews.models import Category, Genre, Review, Title
from users.models import ROLE_CHOICES, User


class GenreSerializer(serializers.ModelSerializer): 

    class Meta:
        model = Genre
        fields = ['name', 'slug']
        read_only_fields = (id,)
        lookup_field = 'slug'


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['name', 'slug']
        read_only_fields = (id,)
        lookup_field = 'slug'



class TitleSerializerMany(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = '__all__'


class TitleSerializerOne(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), many=True, slug_field='slug'
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug'
    )

    class Meta:
        model = Title
        fields = '__all__'

    def validate(self, data):
        if data.get('year') and data.get('year') > timezone.now().year:
            raise serializers.ValidationError(
                'Год выпуска произведения, больше текущего!'
            )
        return data

    def to_representation(self, instance):
        return TitleSerializerMany(instance).data


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    role = serializers.ChoiceField(choices=ROLE_CHOICES)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                f'Имя пользователя не может быть равно {value}'
            )
        return value


class UserSignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'email', 'username',
        )

    def validate(self, attrs):
        if attrs['username'] == 'me':
            raise serializers.ValidationError(
                f'Имя пользователя не может быть равно {attrs["username"]}')
        return super().validate(attrs)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    title = serializers.SlugRelatedField(
        read_only=True,
        slug_field='id'
    )

    class Meta:
        model = Review
        fields = '__all__'
