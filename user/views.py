from rest_framework.response import Response
from rest_framework import status, permissions, generics
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Profile
from .serializers import RegisterSerializer, LoginSerializer
from django.contrib.auth.models import User

class RegisterUserAPIView(APIView):
    """User Registration API View."""
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(request_body=RegisterSerializer)
    def post(self, request):
        """Register a new user."""
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": status.HTTP_201_CREATED,
                "message": "User registered successfully",
                "user":serializer.data
            })
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "errors": serializer.errors
        })

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="user_id",
                in_=openapi.IN_QUERY,
                description="User ID to fetch user details",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ]
    )
    def get(self, request):
        """Retrieve user details using user_id."""
        user_id = request.query_params.get("user_id")

        if not user_id:
            return Response({"error": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
            serializer = RegisterSerializer(user) 
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
    
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="user_id",
                in_=openapi.IN_QUERY,
                description="User ID to fetch user details",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ]
    )
    def delete(self, request):
        """Delete user based on user_id."""
        user_id = request.query_params.get("user_id")

        if not user_id:
            return Response({"error": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
            user.delete()  
            return Response({"message": "User successfully deleted"}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class LoginAPIView(APIView):
    
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]
            user = authenticate(username=username, password=password)

            if user is not None:
                refresh = RefreshToken.for_user(user)
                return Response({
                    "status": status.HTTP_200_OK,
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "user_id": user.id, 
                    "message": "Login successful"
                })
            return Response({
                "status": status.HTTP_401_UNAUTHORIZED,
                "message": "Invalid credentials"
            })
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "errors": serializer.errors
        })

    def get(self, request):
        """Fetch user login details (dummy response)."""
        return Response({"message": "Login endpoint - Provide credentials via POST"}, status=status.HTTP_200_OK)




from .serializers import AdminRegisterSerializer, AdminLoginSerializer


from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class AdminRegisterAPIView(APIView):
    
    permission_classes = [permissions.AllowAny] 

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["username", "email", "password", "password2"],
            properties={
                "username": openapi.Schema(type=openapi.TYPE_STRING, description="Admin username"),
                "email": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL, description="Admin email"),
                "password": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD, description="Password"),
                "password2": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD, description="Confirm Password"),
            },
        ),
        responses={201: "Admin registered successfully", 400: "Bad Request"},
    )
    def post(self, request):
        
        serializer = AdminRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": status.HTTP_201_CREATED,
                "message": "Admin registered successfully",
                "admin": serializer.data
            })
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "errors": serializer.errors
        })

class AdminLoginAPIView(APIView):
    
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["username", "password"],
            properties={
                "username": openapi.Schema(type=openapi.TYPE_STRING, description="Admin username"),
                "password": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD, description="Admin password"),
            },
        ),
        responses={200: "Login successful", 401: "Invalid credentials"},
    )
    def post(self, request):
        
        serializer = AdminLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response({
                "status": status.HTTP_200_OK,
                "message": "Admin login successful",
                "data": serializer.validated_data
            })
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "errors": serializer.errors
        })
        
        
        
class GetAllUsers(APIView):

    def get(self, request):
        users = User.objects.exclude(username="admin", email="admin@gmail.com")
        serializer = RegisterSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)