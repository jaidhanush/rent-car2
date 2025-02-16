from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from .models import Profile  # Import the Profile model

class ProfileSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = Profile
        fields = ["address", "phone_number"]

class RegisterSerializer(serializers.ModelSerializer):


    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    profile = ProfileSerializer()  # ✅ Make it writable

    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "password2", "profile")

    def validate(self, attrs):
        
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
     
    
     profile_data = validated_data.pop("profile", {})  # Extract profile data

     user = User.objects.create_user(
        username=validated_data["username"],
        email=validated_data["email"],
        password=validated_data["password"]
     )

    
     Profile.objects.create(
        user=user,
        address=profile_data.get("address", ""),  
        phone_number=profile_data.get("phone_number", "")  
     )

     return user


class LoginSerializer(serializers.Serializer):
    
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)



class AdminRegisterSerializer(serializers.ModelSerializer):
    

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "password2", "is_staff")

    def validate(self, attrs):
        
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        
        
        validated_data.pop("password2")  

        user = User.objects.create_superuser(  
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"]
        )

        return user


from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class AdminLoginSerializer(serializers.Serializer):
    
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        
        username = attrs.get("username")
        password = attrs.get("password")

        user = authenticate(username=username, password=password)

        if user is None or not user.is_staff: 
            raise serializers.ValidationError({"error": "Invalid admin credentials"})

        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user_id": user.id,
            "username": user.username,
            "is_staff": user.is_staff
        }
