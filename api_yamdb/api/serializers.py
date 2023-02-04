from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers
from reviews.models import Review, Title
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

    def validate(self, value):
        if value == 'me' or value == '':
            raise serializers.ValidationError(
                f'Имя пользователя не может быть равно {value}'
            )
        return value


class UserSignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=254)
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[UnicodeUsernameValidator()])

    class Meta:
        fields = (
            'username', 'email'
        )

    def validate_username(self, value):
        if value == 'me' or value == '':
            raise serializers.ValidationError(
                f'Имя пользователя не может быть равно {value}'
            )
        return value

    def validate(self, attrs):
        user_by_username = User.objects.filter(username=attrs['username'])
        user_by_email = User.objects.filter(email=attrs['email'])
        if (user_by_username.exists
           and user_by_username.first() != user_by_email.first()):
            raise serializers.ValidationError(
                'Пользователь с таким именем или email уже существует'
            )
        return super().validate(attrs)


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True,
        read_only=True, slug_field='slug')
    category = serializers.SlugRelatedField(read_only=True, slug_field='slug')

    class Meta:
        model = Title
        fields = '__all__'


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
