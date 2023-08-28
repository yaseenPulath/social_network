from rest_framework import serializers
from user.models import UserProfile, User
from friends.models import FriendRequest
from datetime import datetime, timedelta as td
from rest_framework.exceptions import ErrorDetail
from user.utils import validate_user_age
from django.utils import timezone

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

class UserSearchSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="id", read_only=True)
    class Meta:
        model = UserProfile
        fields = [
            "user_id", "username", "interests", "about"
        ]

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
        userprofile = UserProfile.objects.get(id=instance.id)
        validated_data['user'] = user
        for field, value in validated_data.items():
            setattr(userprofile, field, value)
        userprofile.save()
        return userprofile

    def validate(self, data):
        data = super().validate(data)
        user_data = data.get("user", {})
        email = user_data.get("email")
        date_of_birth = data.get("date_of_birth")
        if email:
            if email != self.instance.user.email:
                if User.objects.filter(email=email).exists():
                    raise serializers.ValidationError(
                        {"email": ErrorDetail("Email is already taken.", code="unique")}
                    )
        if date_of_birth:
            validate_user_age(date_of_birth)
        return data

class UserProfileFriendRquestSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="id", read_only=True)
    email = serializers.EmailField(source='user.email', required=False)
    class Meta:
        model = UserProfile
        fields = ["user_id", "username", "email"]


class SentAcceptedFriendRequestSerializer(serializers.ModelSerializer):
    request_created_at = serializers.DateTimeField(source="created_at")
    request_accepted_at = serializers.DateTimeField(source="updated_at")
    to_user = UserProfileFriendRquestSerializer(read_only=True)
    class Meta:
        model = FriendRequest
        fields = ["request_created_at", "request_accepted_at", "to_user"]

class ReceivedPendingRequestSerializer(serializers.ModelSerializer):
    request_created_at = serializers.DateTimeField(source="created_at")
    from_user = UserProfileFriendRquestSerializer(read_only=True)
    days_since_updated = serializers.SerializerMethodField()
    class Meta:
        model = FriendRequest
        fields = ["request_created_at", "from_user", "status", "days_since_updated"]

    def get_days_since_updated(self, instance):
        if instance.updated_at:
            current_datetime = timezone.now()
            delta = current_datetime - instance.updated_at
            return delta.days
        return None