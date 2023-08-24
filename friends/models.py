from django.db import models
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

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f"From: {self.from_user.user.username}, To: {self.to_user.user.username}"


class Friendship(Timestamped):
    user1 = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='friendships_as_user1')
    user2 = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='friendships_as_user2')
    active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user1', 'user2')

    def __str__(self):
        return f"{self.user1.user.username} - {self.user2.user.username}"
