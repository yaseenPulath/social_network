# from django.urls import path, include
# from user.views import UserRegistrationView, UserLoginView, UserOperationsViewSet
# from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r'', UserOperationsViewSet, basename='user')

# urlpatterns = [
#     path('register/', UserRegistrationView.as_view(), name="user_registration"),
#     path('login/', UserLoginView.as_view(), name="user_login"),
#     # path('change_password/', include('user.urls')),
#     # path('update_profile/', include('user.urls')),
# ] + router.urls