from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.models import Profile


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'bio', 'location', 'birth_date',)


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'profile',)
