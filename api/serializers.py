from rest_framework import serializers
from django.contrib.auth.models import User
from user.models import UserProfile
from friends.models import FriendRequest, Friendship
from datetime import datetime, timedelta as td

class JWTPayloadSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email']

    def to_representation(self, obj):
        data = super().to_representation(obj)
        extra_fields = {
             'iss': 'social-network',
             'iat': int(datetime.now().timestamp()),
             'exp': int((datetime.now() + td(days=1)).timestamp())
        }
        data = {**data, **extra_fields}
        return data

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class SentAcceptedFriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = '__all__'

class ReceivedPendingRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = '__all__'
