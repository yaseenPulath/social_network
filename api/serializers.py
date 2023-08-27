from rest_framework import serializers
from user.models import UserProfile, User
from friends.models import FriendRequest
from datetime import datetime, timedelta as td
from rest_framework.exceptions import ErrorDetail

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
    user_id = serializers.IntegerField(source="id", read_only=True)
    email = serializers.EmailField(source='user.email', required=False)
    password = serializers.CharField(source="user.password", write_only=True, required=False)
    class Meta:
        model = UserProfile
        fields = [
            "user_id", "username", "email", "password", "date_of_birth",
            "gender", "interests", "about"
        ]
        extra_kwargs = {
            'gender': {
                'error_messages': {
                    'invalid_choice': 'Valid choices are: Male, Female, Other.'
                }
            }
        }

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        password = user_data.pop('password', None)
        email = user_data.pop('email', None)
        user = instance.user
        if email:
            user.email = email
        if password:
            user.set_password(password)
        user.save()
        userprofile = UserProfile.objects.filter(id=instance.id)
        userprofile.update(user=user, **validated_data)
        instance = userprofile.last()
        return instance

    def validate(self, data):
        data = super().validate(data)
        user_data = data.get("user", {})
        email = user_data.get("email")
        if email:
            if email != self.instance.user.email:
                if User.objects.filter(email=email).exists():
                    raise serializers.ValidationError(
                        {"email": ErrorDetail("Email is already taken.", code="unique")}
                    )
        return data


class SentAcceptedFriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = '__all__'

class ReceivedPendingRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = '__all__'
