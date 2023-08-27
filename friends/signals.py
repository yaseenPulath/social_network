from django.db.models.signals import post_save
from django.dispatch import receiver
from friends.models import FriendRequest, Friendship

@receiver(post_save, sender=FriendRequest)
def create_friendship(sender, instance, **kwargs):
    if instance.status == 'accepted':
        Friendship.objects.get_or_create(user1=instance.from_user, user2=instance.to_user, active=True)
