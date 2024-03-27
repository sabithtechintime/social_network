from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

UserModel = get_user_model()


FRIEND_REQUEST_STATUS = (
    (0, "requested",),
    (1, "accepted",),
    (2, "rejected")
)


class FriendRequest(models.Model):
    sender = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    recipient = models.ForeignKey(UserModel, related_name='friend_requests', on_delete=models.CASCADE)
    status = models.IntegerField(choices=FRIEND_REQUEST_STATUS, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def get_requests_count(cls, user):
        # Count the number of requests sent by the user within the last minute
        one_minute_ago = timezone.now() - timezone.timedelta(minutes=1)
        return cls.objects.filter(sender=user, created_at__gte=one_minute_ago).count()

