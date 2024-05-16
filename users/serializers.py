from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import User, Patient


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'phone_number',
            'user_roles',
            'region',
            'created_at',
            'password',
        )
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'phone_number': {'required': True},
            'user_roles': {'required': False}
        }

    def create(self, validated_data):
        user = super(RegisterSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate(self, data):
        phone_number = data.get('phone_number')
        print('salom')
        if phone_number and User.objects.filter(phone_number=phone_number).exists():
            raise ValidationError({'username': 'Username already exists'})

        return data


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'phone_number', 'password')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'phone_number',
            'user_roles',
            'region',
            'created_at'
        )


class AddToPatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'sender', 'doctor', 'patient', 'created_at']
