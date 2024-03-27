from django.urls import path
from friend.views import CreateFriendRequest, AcceptFriendRequest, RejectFriendRequest, FriendRequests


urlpatterns = [
    path('send/<int:user_id>', CreateFriendRequest.as_view(), name='send-friend-request'),
    path('accept/<int:pk>/', AcceptFriendRequest.as_view(), name='accept-friend-request'),
    path('reject/<int:pk>/', RejectFriendRequest.as_view(), name='reject-friend-request'),
    path('pending', FriendRequests.as_view(), name='pending-friend-request'),
]