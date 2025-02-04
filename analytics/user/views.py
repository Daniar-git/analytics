from .serializers import UserSerializer, UserDetailsSerializer, UserUpdateSerializer, TokenSerializer
from .models import User

from dj_rest_auth.models import TokenModel
from dj_rest_auth.views import UserDetailsView
from dj_rest_auth.registration.views import RegisterView

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_tracking.mixins import LoggingMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework.parsers import FileUploadParser

# Create your views here.


class UserView(LoggingMixin, UserDetailsView):
    """
       patch:
       Update user

       ---

       get:
       Return user

       ---

       put:
       Update user

       ---
       """
    serializer_class = UserUpdateSerializer
    queryset = User.objects.all()
    pagination_class = PageNumberPagination
    parser_class = (FileUploadParser)

    def update(self, request, *args, **kwargs):
        serializer_class = UserUpdateSerializer
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data
        if 'username' in data:
            if User.objects.filter(username=data['username']):
                return Response({"message": "Username is already taken"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = serializer_class(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return Response({"status": True}, status=status.HTTP_200_OK)


class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = self.request.user
        serializer = UserDetailsSerializer(user)
        return Response(serializer.data)


class UserTokenInfo(APIView):

    def post(self, request, *args, **kwargs):
        key = request.data.get('key')
        token = TokenModel.objects.filter(key=key).first()
        if not token:
            return Response({"status": "user not found"}, status=400)
        return Response(UserSerializer(token.user).data, status=200)



class UserRegisterView(LoggingMixin, RegisterView):

    def get_response_data(self, user):
        token, _ = TokenModel.objects.get_or_create(user=user)
        return TokenSerializer(user.auth_token, context=self.get_serializer_context()).data