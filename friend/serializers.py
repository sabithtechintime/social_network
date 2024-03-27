from rest_framework import serializers

from friend.models import FriendRequest


class FriendRequestSerializer(serializers.ModelSerializer):
    sender_username = serializers.SerializerMethodField()
    sender_email = serializers.SerializerMethodField()

    class Meta:
        model = FriendRequest
        fields = ['id', 'sender_username', 'sender_email']

    def get_sender_username(self, obj):
        return obj.sender.username if obj.sender else None

    def get_sender_email(self, obj):
        return obj.sender.email if obj.sender else None


class FriendRequestSendSerializer(serializers.ModelSerializer):
    recipient_username = serializers.SerializerMethodField()
    recipient_email = serializers.SerializerMethodField()

    class Meta:
        model = FriendRequest
        fields = ['id', 'sender_username', 'sender_email']

    def get_recipient_username(self, obj):
        return obj.recipient.username if obj.recipient else None

    def get_recipient_emaill(self, obj):
        return obj.recipient.email if obj.recipient else None


# class FriendRequestAcceptRejectSerializer(serializers.Serializer):
#     request_id = serializers.IntegerField()
#     action = serializers.
