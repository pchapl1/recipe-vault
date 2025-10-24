from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.timezone import now
from .serializers import RegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from datetime import datetime, timezone
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        # Calculate expiration times
        access_expires = access_token['exp']
        refresh_expires = refresh['exp']

        return Response({
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            },
            "access": str(access_token),
            "access_expires": access_expires,     # ⏳ UNIX timestamp
            "refresh": str(refresh),
            "refresh_expires": refresh_expires,   # ⏳ UNIX timestamp
        }, status=status.HTTP_201_CREATED)



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Customize token response to include expiration info."""

    def validate(self, attrs):
        data = super().validate(attrs)

        # Access the tokens
        refresh = self.get_token(self.user)
        access_token = refresh.access_token

        # Add expiration timestamps
        data['access_expires'] = datetime.fromtimestamp(access_token['exp'], tz=timezone.utc).isoformat()
        data['refresh_expires'] = datetime.fromtimestamp(refresh['exp'], tz=timezone.utc).isoformat()

        # Add user info
        data['user'] = {
            "id": self.user.id,
            "username": self.user.username,
            "email": self.user.email,
        }

        return data



class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()   # 👈 this blacklists the refresh token
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({"detail": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)




