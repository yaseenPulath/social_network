from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
# from rest_framework.pagination import PageNumberPagination
from user.models import UserProfile
from user.utils import generate_secure_password
from api.serializers import JWTPayloadSerializer, UserRegistrationSerializer, SentAcceptedFriendRequestSerializer, \
    ReceivedPendingRequestSerializer, UserProfileSerializer, UserSearchSerializer
from user.jwt_utils import generate_jwt_token
from django.contrib.auth import authenticate
from django.db import IntegrityError
from rest_framework.exceptions import PermissionDenied
from api.authentication import JWTAuthentication
from api.permissions import JWTPermission
from api.pagination import CustomPagination
from api.throttles import FriendRequestThrottle
from friends.models import FriendRequest

class UserRegistrationView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if email:
            try:
                user_profile = UserProfile.objects.create_userprofile_with_user(email=email)
                user = user_profile.user
                serializer = UserRegistrationSerializer(user)
                payload = JWTPayloadSerializer(user).data
                token = generate_jwt_token(payload)
                data = serializer.data
                data['token'] = token
                response_data = {
                    "status": "Success",
                    'message': 'User registered successfully. please update password to avoid security risks.',
                    "detail": data
                }
                return Response(response_data, status=status.HTTP_201_CREATED)
            except IntegrityError as e:
                return Response({"status": "Failure", "message": e.args[0]}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                # logger
                return Response({"status": "Failure", "message": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)
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
                "detail": {'token': token, **serializer.data}
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
    serializer_class = UserProfileSerializer
    pagination_class = CustomPagination
    pagination_class.page_size = 10
    pagination_class.max_page_size = 100


    def get_serializer(self, *args, **kwargs):
        if self.action == "retrieve":
            return UserSearchSerializer(*args, **kwargs)
        return self.serializer_class(*args, **kwargs)
        

    def change_password(self, request):
        data = request.data
        new_password = data.get("password")
        if new_password:
            user = request.user
            user.set_password(new_password)
            user.is_registration_completed = True
            user.save()
            return Response({"status": "Success", "message": "Password changed successfully."})
        else:
            return Response({
                "status": "Failure",
                "message": "password can't me empty"
            }, status=status.HTTP_400_BAD_REQUEST)
    
    def update_profile(self, request):
        data = self.request.data
        user_profile = request.user.userprofile
        serializer = self.get_serializer(user_profile, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "Success", "message": "Profile updated successfully.", "detail": serializer.data}, status=status.HTTP_200_OK)
        return Response({"status": "Failure", "Errors": serializer.errors, "message": "Please provide a valid data"}, status=status.HTTP_400_BAD_REQUEST)


    def partial_update(self, request, pk):
        '''
        used for change password and update profile
        '''
        action = pk
        if action == "change-password":
            return self.change_password(self.request)
        if action == "update-profile":
            return self.update_profile(self.request)


    def retrieve(self, request, pk, *args, **kwargs):
        '''
        to search users
        '''
        email = request.query_params.get('email', '')
        name = request.query_params.get('name', '')
        request_user = request.user

        queryset = UserProfile.objects.none()
        match_detail = {}
        if email:
            match_detail["is_exact_match"] = True
            queryset = UserProfile.objects.filter(user__email=email).exclude(user__id=request_user.id)
            if not queryset.exists():
                match_detail["is_exact_match"] = False
                queryset = UserProfile.objects.filter(user__email__icontains=email).exclude(user__id=request_user.id)
        elif name:
            match_detail["is_exact_match"] = True
            queryset = UserProfile.objects.filter(user_name=name).exclude(user__id=request_user.id)
            if not queryset.exists():
                match_detail["is_exact_match"] = False
                queryset = UserProfile.objects.filter(user_name__icontains=name).exclude(user__id=request_user.id)
        
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.get_serializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data, match_detail)


class FriendRequestViewSet(ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_classes = [FriendRequestThrottle]
    pagination_class = PageNumberPagination
    pagination_class.page_size = 10
    pagination_class.max_page_size = 100

    def get_permission_class(self):
        if self.action == 'partial_update':
            return JWTPermission
        return IsAuthenticated
    
    def get_serializer(self, *args, **kwargs):
        if self.action == "sent_accepted_requests":
            return SentAcceptedFriendRequestSerializer(*args, **kwargs)
        if self.action == "received_pending_requests":
            return ReceivedPendingRequestSerializer(*args, **kwargs)
        if self.action == "partial_update":
            return UserProfileSerializer(*args, **kwargs)
        
        return self.serializer_class(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        data = request.data
        user_id = data.get("user_id")
        if user_id:
            from_user = request.user.userprofile
            try:
                to_user = UserProfile.objects.get(id=user_id)
            except UserProfile.DoesNotExist:
                return Response({"status": "Failure", "message": "User Not Found."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if from_user.has_friendship_with(to_user):
                return Response({"status": "Failure", "message": "You are already connected with this user as a friend."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if FriendRequest.has_open_friend_request(from_user, to_user):
                friend_request = FriendRequest.get_open_friend_requests(from_user, to_user).last()
                return Response({"status": "Failure", "message": "There is already an open friend request between you and this user.", "detail": {"request_id": friend_request.id}},
                    status=status.HTTP_400_BAD_REQUEST
                )
            try:
                friend_request = FriendRequest.objects.create(from_user=from_user, to_user=to_user)
                return Response({"status": "Success", "message": "Friend request sent successfully.", "detail": {"request_id": friend_request.id}},
                                status=status.HTTP_201_CREATED)
            except Exception as e:
                # logger
                return Response({"status": "Failure", "message": "Something went wrong."},
                    status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": "Failure", "message": "user_id is mandatory to send friend request."},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def accept_request(self, request, request_id):
        try:
            to_user = request.user.userprofile
            friend_request = FriendRequest.objects.get(id=request_id, status="sent")
            from_user = friend_request.from_user
            friend_request.status = "accepted"
            friend_request.save()
            serialiser = self.get_serializer(from_user)
            return Response({"status": "Success", "message": "Friend request accepted successfully.", "detail":serialiser.data}, status=status.HTTP_200_OK)
        except FriendRequest.DoesNotExist as e:
            return Response({"status": "Failure", "message": "Friend Request Not Found"},status = status.HTTP_400_BAD_REQUEST)        

    def reject_request(self, request, request_id):
        # TO DO: block user and reject request
        try:
            to_user = request.user.userprofile
            friend_request = FriendRequest.objects.get(id=request_id, status="sent")
            from_user = friend_request.from_user
            friend_request.status = "rejected"
            friend_request.save()
            return Response({"status": "Success", "message": "Friend request rejected successfully."}, status=status.HTTP_202_ACCEPTED)
        except FriendRequest.DoesNotExist as e:
            return Response({"status": "Failure", "message": "Friend Request Not Found"},status = status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        data = request.data
        update_action = data.get("action")
        if update_action:
            request_id = pk
            permission_class = self.get_permission_class()
            try:
                if permission_class.has_permission(permission_class, request, self, data={"action":"recieved-friend-request", "request_id": request_id}):
                    if update_action == "accept-request":
                        return self.accept_request(request, request_id)
                    if update_action == "reject-request":
                        return self.reject_request(request, request_id)
                return Response({"status": "Failure", "message": "You are not authorized to perform this action."},
                    status=status.HTTP_401_UNAUTHORIZED)
            except FriendRequest.DoesNotExist as e:
                return Response({"status": "Failure", "message": "Friend Request Not Found"},status = status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                # logger
                return Response({"status": "Failure", "message": "Something went wrong."},
                                status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": "Failure", "message": "Couldn't find any action to perform."},
                status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"], url_path="sent-accepted")
    def sent_accepted_requests(self, request):
        user = request.user.userprofile 
        accepted_friend_requests = FriendRequest.objects.filter(from_user=user, status="accepted", active=False)

        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(accepted_friend_requests, request)
        serializer = self.get_serializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    @action(detail=False, methods=["get"], url_path="received-pending")
    def received_pending_requests(self, request):
        user = request.user.userprofile
        pending_friend_requests = FriendRequest.objects.filter(to_user=user, status="sent", active=True)

        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(pending_friend_requests, request)
        serializer = self.get_serializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

#TO DO: UNFRIEND, UNFRIEND AND BLOCK 
