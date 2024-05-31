from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

from users.serializers import UserSerializer, CreateUserSerializer, MyTokenObtainSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView, TokenViewBase
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CreateUserView(CreateAPIView):
    model = get_user_model()
    queryset = model.objects.all()
    #permission_classes = (IsAnonymousUser, )
    serializer_class = CreateUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        print('//******', serializer.data)
        response_data = {
            'id': serializer.data.get('id'),
            'email': serializer.data.get('email'),
        }
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)


class UserListView(ListAPIView):
    model = get_user_model()
    queryset = model.objects.all()
    serializer_class = UserSerializer


class RetrieveUpdateUserView(RetrieveUpdateAPIView):
    model = get_user_model()
    queryset = model.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        pk = request.user.pk
        return self.retrieve(request, pk, *args, **kwargs)

    def put(self, request, *args, **kwargs):

        return self.update(request, *args, **kwargs)


class MyTokenObtainPairView(TokenViewBase):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """
    serializer_class = MyTokenObtainSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        print('*****', serializer.validated_data)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
