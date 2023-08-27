from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.throttling import UserRateThrottle
from rest_framework.pagination import PageNumberPagination
from user.models import UserProfile
from user.utils import generate_secure_password
from api.serializers import JWTPayloadSerializer, UserRegistrationSerializer, SentAcceptedFriendRequestSerializer, \
    ReceivedPendingRequestSerializer, UserProfileSerializer
from user.jwt_utils import generate_jwt_token
from django.contrib.auth import authenticate
from api.authentication import JWTAuthentication
from friends.models import FriendRequest

class UserRegistrationView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if email:
            try:
                user_profile = UserProfile.objects.create_userprofile_with_user(email=email, password=password)
                user = user_profile.user
            except Exception as e:
                # logger
                return Response({"message": "User Already exists."}, status=status.HTTP_400_BAD_REQUEST)
            serializer = UserRegistrationSerializer(user)
            response_data = {
                "status": "Success",
                'message': 'User registered successfully. Please update your password within 24 hours.' if user_profile.is_auto_generated_password else 'User registered successfully.',
                **serializer.data
            }
            if user_profile.is_auto_generated_password:
                payload = JWTPayloadSerializer(user).data
                token = generate_jwt_token(payload)
                response_data['token'] =  token
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response({"status": "Failure", "message": "Email is mandatory for registration"}, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(email=email, password=password)
        if user:
            payload = JWTPayloadSerializer(user).data
            token = generate_jwt_token(payload)
            serializer = UserRegistrationSerializer(user)
            response_data = {
                "status": "Success",
                'message': 'User logged in successfully.',
                'token': token,
                **serializer.data
            }
            return Response(response_data, )
        else:
            return Response(
                {"status": "Failure", "message": "Invalid credentials. Please try again."},
                status=status.HTTP_400_BAD_REQUEST
            )

class UserOperationsViewSet(ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = UserProfile.objects.all()
    pagination_class = PageNumberPagination
    pagination_class.page_size = 10
    pagination_class.max_page_size = 100

    def get_serializer(self, *args, **kwargs):
        if self.action in ['search_users', 'update_profile']:
            return UserProfileSerializer(*args, **kwargs)
        return super().get_serializer(*args, **kwargs)

    @action(detail=False, methods=['patch'], url_path='update-profile')
    def update_profile(self, request):
        data = self.request.data
        user_profile = request.user.userprofile
        serializer = self.get_serializer(user_profile, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "Success", "message": "Profile updated successfully.", **serializer.data})
        return Response({"status": "Failure", "Errors": serializer.errors, "message": "Please provide a valid data"})

    @action(detail=False, methods=['patch'], url_path='change-password')
    def change_password(self, request   ):
        data = request.data
        new_password = data.get("password")
        if new_password:
            user = request.user
            user.set_password(new_password)
            user.save()
            return Response({"status": "Success", "message": "Password changed successfully."})
        else:
            return Response({
                "status": "Failure",
                "message": "password can't me empty"
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], url_path='search-users', permission_classes=[IsAuthenticated])
    def search_users(self, request):
        email = request.query_params.get('email', '')
        name = request.query_params.get('name', '')

        queryset = UserProfile.objects.none()
        is_exact_match = True
        if email:
            queryset = UserProfile.objects.filter(user__email=email)
            if not queryset.exists():
                is_exact_match = False
                queryset = UserProfile.objects.filter(user__email__icontains=email)
        elif name:
            queryset = UserProfile.objects.filter(user_name=name)
            if not queryset.exists():
                is_exact_match = False
                queryset = UserProfile.objects.filter(user_name__icontains=name)
        if is_exact_match:
            instance = queryset.last()
            serializer = self.get_serializer(instance)
    
        else:
            paginator = self.pagination_class()
            paginated_queryset = paginator.paginate_queryset(queryset, request)
            serializer = self.get_serializer(paginated_queryset, many=True)
            return paginator.get_paginated_response(serializer.data)
        return Response(serializer.data)


class FriendRequestViewSet(ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


    @action(detail=True, methods=['post'], url_path='send-request', throttle_classes=[UserRateThrottle])
    def send_request(self, request, pk=None):
        from_user = request.user.userprofile
        to_user = UserProfile.objects.get(id=pk)
        if from_user.has_friendship_with(to_user):
            return Response({"message": "You are already connected with this user as a friend."},
                status=status.HTTP_400_BAD_REQUEST
            )
        if FriendRequest.has_open_friend_request(from_user, to_user):
            return Response({"message": "There is already an open friend request between you and this user."},
                status=status.HTTP_400_BAD_REQUEST
            ) 
        friend_request = FriendRequest.objects.create(from_user=from_user, to_user=to_user)
        return Response({"message": "Friend request sent successfully."}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], url_path='accept-request')
    def accept_request(self, request, pk=None):
        from_user = UserProfile.objects.get(id=pk)
        to_user = request.user.userprofile
        try:
            friend_request = FriendRequest.objects.get(from_user=from_user, to_user=to_user, status="sent")
        except Exception as e:
            # loger
            return Response({"message": "Friend Request Not Found"},status = status.HTTP_400_BAD_REQUEST)
        friend_request.status = "accepted"
        friend_request.save()
        return Response({"message": "Friend request accepted successfully.."}, status=status.HTTP_202_ACCEPTED)

    @action(detail=True, methods=['post'], url_path='reject-request')
    def reject_request(self, request, pk=None):
        # TO DO: block user and reject request
        from_user = UserProfile.objects.get(id=pk)
        to_user = request.user.userprofile
        try:
            friend_request = FriendRequest.objects.get(from_user=from_user, to_user=to_user, status="sent")
        except Exception as e:
            # logger
            return Response({"message": "Friend Request Not Found"},status = status.HTTP_400_BAD_REQUEST)
        friend_request.status = "rejected"
        friend_request.save()
        return Response({"message": "Friend request rejected successfully."}, status=status.HTTP_202_ACCEPTED)

    @action(detail=False, methods=["get"], url_path="sent-accepted")
    def sent_accepted_requests(self, request):
        user = request.user.userprofile 
        accepted_friend_requests = FriendRequest.objects.filter(from_user=user, status="accepted", active=False)
        serializer = SentAcceptedFriendRequestSerializer(accepted_friend_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=["get"], url_path="received-pending")
    def received_pending_requests(self, request):
        user = request.user.userprofile
        pending_friend_requests = FriendRequest.objects.filter(to_user=user, status="sent", active=True)
        serializer = ReceivedPendingRequestSerializer(pending_friend_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#TO DO: UNFRIEND, UNFRIEND AND BLOCK 
