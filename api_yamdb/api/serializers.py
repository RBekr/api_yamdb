from users.models import User
from users.models import ROLE_CHOICES
from rest_framework import serializers

class UserSerializers(serializers.ModelSerializer):
    role =  serializers.ChoiceField(choices=ROLE_CHOICES)
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(f'Имя пользователя не может ровняться {value}')
        return value