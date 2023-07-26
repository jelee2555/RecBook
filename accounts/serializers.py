from .models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    User.id = User.user_id

    class Meta:
        model = User
        fields = '__all__'