from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status, authentication
from django.contrib.auth import get_user_model

from friend.serializers import FriendRequestSerializer, FriendRequestSendSerializer
from friend.models import FriendRequest

UserModel = get_user_model()


class FriendRequests(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        friend_requests = FriendRequest.objects.filter(recipient=request.user, status=0)
        serializer = FriendRequestSerializer(friend_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateFriendRequest(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        sender = request.user
        recipient = get_object_or_404(UserModel, pk=user_id)

        # Check if the user has exceeded the limit for friend requests within the last minute
        if FriendRequest.get_requests_count(sender) >= 3:
            return Response(
                {'error': 'You cannot send more than 3 friend requests within a minute.'},
                status=status.HTTP_400_BAD_REQUEST
        )
        friend_request, created = FriendRequest.objects.get_or_create(sender=sender, recipient=recipient)
        if not created:
            return Response(
                {
                    'error': f'Friend request already exists'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = FriendRequestSendSerializer(friend_request)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AcceptFriendRequest(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        friend_request = get_object_or_404(FriendRequest, pk=pk, recipient=request.user.id)
        if friend_request:
            if friend_request.status == 0:
                friend_request.sender.friends.add(friend_request.recipient)
                friend_request.recipient.friends.add(friend_request.sender)
                friend_request.status = 1
                friend_request.save()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(
                    {
                        'error': f'Invalid Operation, Friend request already accepted or rejected'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        return Response({"error": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)


class RejectFriendRequest(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        friend_request = get_object_or_404(FriendRequest, pk=pk, recipient=request.user)
        if friend_request:
            if friend_request.status == 0:
                friend_request.status = 2
                friend_request.save()
                return Response(
                    {"message": "Successfully rejected the request"},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        'error': f'Invalid Operation, Friend request already accepted or rejected'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        return Response({"error": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)
