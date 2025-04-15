from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.serializers import ModelSerializer, EmailField, CharField, ValidationError
from rest_framework.validators import UniqueValidator


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "date_joined"]


class RegisterSerializer(ModelSerializer):
    email = EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])

    password = CharField(write_only=True, required=True, validators=[validate_password])
    password2 = CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("email", "password", "password2")
        extra_kwargs = {"first_name": {"required": False}, "last_name": {"required": False}}

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(username=validated_data["email"], email=validated_data["email"])

        user.set_password(validated_data["password"])
        user.save()

        return user
