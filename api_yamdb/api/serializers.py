from rest_framework import serializers
from reviews.models import Review, Title
from users.models import ROLE_CHOICES, User


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(many=True,
        read_only=True, slug_field='slug')
    category = serializers.SlugRelatedField(read_only=True, slug_field='slug')

    class Meta:
        model = Title
        fields = '__all__'


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

