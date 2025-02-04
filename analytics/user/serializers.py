from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from dj_rest_auth.models import TokenModel

from .models import User


class UserSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        exclude_fields = kwargs.pop('exclude_fields', None)
        super(UserSerializer, self).__init__(*args, **kwargs)
        # if self.context and 'view' in self.context and self.context['view'].__class__.__name__ == 'UsersView':
        #     exclude_fields = ['file']
        if self.context and 'exclude_fields' in self.context:
            exclude_fields = self.context['exclude_fields']
        if exclude_fields:
            for field_name in exclude_fields:
                self.fields.pop(field_name)

    class Meta:
        exclude = ('password', 'last_login', 'is_superuser', 'is_staff', 'date_joined')
        model = User



class UserRegistrationSerializer(RegisterSerializer):
    first_name = serializers.CharField(write_only=True, required=False)
    last_name = serializers.CharField(write_only=True, required=False)

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'email': self.validated_data.get('email', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
        }



class UserDetailsSerializer(serializers.ModelSerializer):
    key = serializers.SerializerMethodField('is_key', read_only=True)
    user = serializers.SerializerMethodField('is_user', read_only=True)

    def is_key(self, obj):
        token = TokenModel.objects.filter(user=obj).first()
        if not token:
            token = TokenModel.objects.create(user=obj)
        return str(token)

    def is_user(self, obj):
        serializers = UserSerializer(obj)
        return serializers.data


    class Meta:
        fields = ('user', 'key')
        model = User


class TokenSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = TokenModel
        fields = '__all__'


class UserUpdateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']