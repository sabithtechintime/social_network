from django.contrib.auth import get_user_model, login, logout
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import authentication, permissions, status

from core.serializers import (
    UserLoginSerializer,
    UserRegisterSerializer,
    UserSerializer
)

UserModel = get_user_model()


class CustomAuthToken(ObtainAuthToken):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.check_user(serializer.validated_data)
            if not user:
                return Response({"error": "invalid user credentials"}, status=status.HTTP_400_BAD_REQUEST)
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'email': user.email
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class UserRegister(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.create(serializer.validated_data)
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    permissions = [permissions.AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.check_user(serializer.validated_data)
            login(request, user)
            return Response(serializer.data, status=status.HTTP_200_OK)


class UserLogout(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class FriendsList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        print(request.user)
        friends_list = UserModel.objects.get(id=request.user.id).friends_list.all()
        serializer = UserSerializer(friends_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SearchUser(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        search_keyword = request.GET.get('q')

        # Query users by email (exact match)
        exact_email_match = UserModel.objects.filter(email__iexact=search_keyword)
        # Query users by name (contains match)
        name_contains_match = UserModel.objects.filter(username__icontains=search_keyword)
        # Combine the results
        search_results = list(exact_email_match) + list(name_contains_match)
        serializer = UserSerializer(search_results, many=True)
        print(serializer)

        return Response(serializer.data, status=status.HTTP_200_OK)