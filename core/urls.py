from django.urls import path

from core.views import UserLogin, UserLogout, UserRegister, FriendsList, CustomAuthToken, SearchUser

urlpatterns = [

    path('register/', UserRegister.as_view(), name='register'),
    path('login/',CustomAuthToken.as_view(), name='login'),
    path('logout/', UserLogout.as_view(), name='logout'),
    path('friends/', FriendsList.as_view(), name='friends-list'),
    path('search/', SearchUser.as_view(), name='search-user')
]