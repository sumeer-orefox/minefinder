from .serializers import UserSerializer
from users.models import User
from rest_framework import generics

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer