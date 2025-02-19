from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


User = get_user_model()

class RegisterSerilizer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    email = serializers.EmailField(
        required=True,
        validators = [UniqueValidator(queryset=User.objects.all())]
        )
    
    phone_number = serializers.CharField(
        required=True,
        validators = [UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    
    role = serializers.ChoiceField(
        choices=User.ROLE_CHOICES,
        default= User.DEFAULT_ROLE,
        required= False
    )


    class Meta:
        model = User
        fields = ('first_name','email','phone_number','password','confirm_password','role')


    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError('password do not match')     

        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')   

        user = User.objects.create_user(**validated_data)    
        return user




class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['role'] = user.role
        token['phone_number'] = user.phone_number


        return token
    

