from django.urls import include, path

# from social_network.api.v1 import views
from . import  views

urlpatterns = [
    path('user/', include('core.urls')),
    path('friend-requests/', include('friend.urls')),

]