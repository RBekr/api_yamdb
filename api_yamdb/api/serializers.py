from reviews.models import Title
from rest_framework import serializers


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(many=True,
        read_only=True, slug_field='slug')
    category = serializers.SlugRelatedField(read_only=True, slug_field='slug')

    class Meta:
        model = Title
        fields = '__all__'