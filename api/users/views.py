from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView

from users.serializers import UserSerializer


# Create your views here.
class CreateUserView(CreateAPIView):
    model = get_user_model()
    queryset = model.objects.all()
    #permission_classes = (IsAnonymousUser, )
    serializer_class = UserSerializer


class UserListView(ListAPIView):
    model = get_user_model()
    queryset = model.objects.all()
    serializer_class = UserSerializer