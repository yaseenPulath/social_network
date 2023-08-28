from rest_framework.permissions import BasePermission
from friends.models import FriendRequest

class JWTPermission(BasePermission):
    '''
    for now this permission only handle recieved-friend-request
    in future we can add other actions with appropriate checks
    '''
    
    def has_permission(self, request, view, data):
        try:
            action = data.get("action")
            if action == "recieved-friend-request":
                friend_request_id = data.get("request_id")
                friend_request = FriendRequest.objects.get(id=friend_request_id)
                if request.user and request.user.userprofile == friend_request.to_user:
                    return True
        except FriendRequest.DoesNotExist:
            raise FriendRequest.DoesNotExist("Friend Request Not Found")