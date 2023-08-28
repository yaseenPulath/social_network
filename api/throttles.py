from rest_framework.throttling import UserRateThrottle

class FriendRequestThrottle(UserRateThrottle):
    def allow_request(self, request, view):
        if view.action == 'create':
            return super().allow_request(request, view)
        return True
