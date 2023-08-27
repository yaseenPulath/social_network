from django.db import models
from django.db.models import Q
from user.models import UserProfile
from social_network.models import Timestamped

class FriendRequest(Timestamped):
    STATUS_CHOICES = [
        ('sent', 'Sent'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    from_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sent_friend_requests')
    to_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='received_friend_requests')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='sent')
    active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('from_user', 'to_user', 'status', "active")

    def __str__(self):
        return f"To: {self.to_user.user.email}({self.status})"

    @classmethod
    def friend_request_list(cls, userprofile):
        return FriendRequest.objects.filter(Q(from_user=userprofile)|Q(to_user=userprofile)).exclude(
            active = False
        )

    @classmethod
    def get_open_friend_requests(cls, from_user, to_user):
        return FriendRequest.objects.filter(
            Q(from_user=from_user, to_user=to_user, status="sent", active=True) |
            Q(from_user=to_user, to_user=from_user, status="sent", active=True)
        )

    @classmethod
    def has_open_friend_request(cls, from_user, to_user):
        return FriendRequest.get_open_friend_requests(from_user, to_user).exists()

    def save(self, *args, **kwargs):
        if self.status in ["accepted", "rejected"]:
            self.active = False
        super(FriendRequest, self).save(*args, **kwargs)

class Friendship(Timestamped):
    user1 = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='friendships_as_user1')
    user2 = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='friendships_as_user2')
    active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user1', 'user2')

    def __str__(self):
        return self.email

    def __str__(self):
        return f"{self.user1.user.email} - {self.user2.user.email}"
