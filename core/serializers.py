from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate


UserModel = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = '__all__'

    def create(self, validated_data):
        user_obj = UserModel.objects.create(
            email=validated_data['email']
        )
        user_obj.set_password(validated_data['password'])
        user_obj.username = validated_data.get('username', "")
        user_obj.save()
        return user_obj


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def check_user(self, validated_data):
        user = authenticate(
            username=validated_data['email'],
            password=validated_data['password'])
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['id', 'email', 'username']


class UserListSerializer(serializers.Serializer):
    users = serializers.ListField(child=UserSerializer(many=True))




