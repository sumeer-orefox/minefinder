from rest_framework import serializers
from users.models import User,UserProfile
from django.db import models
from message_control.serializers import GenericFileUploadSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__" 
        #exclude = ("password", )  

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
   # username = serializers.CharField()
    password = serializers.CharField()


class RefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    profile_picture = GenericFileUploadSerializer(read_only=True)
    profile_picture_id = serializers.IntegerField(
        write_only=True, required=False)
    message_count = serializers.SerializerMethodField("get_message_count")
   
    
    class Meta:
        model = UserProfile
        fields = "__all__"    

    def get_message_count(self, obj):
        try:
            user_id = self.context["request"].user.id
        except Exception as e:
            user_id = None

        from message_control.models import Message
        message = Message.objects.filter(sender_id=obj.user.id, receiver_id=user_id, is_read=False).distinct()

        return message.count()


class FavoriteSerializer(serializers.Serializer):
    favorite_id = serializers.IntegerField()
    
