from django.urls import path, include
from api.views import UserRegistrationView, UserLoginView, UserOperationsViewSet, FriendRequestViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)
router.register(r'user', UserOperationsViewSet, basename='user')
router.register(r'friend-request', FriendRequestViewSet, basename='friend-request')

urlpatterns = [
    path('user/register/', UserRegistrationView.as_view(), name="register"),
    path('user/login/', UserLoginView.as_view(), name="user_login"),
] + router.urls