from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_400_BAD_REQUEST

from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserSerializer

# Create your views here.
class RegisterView(APIView):
    permission_classes= (AllowAny,)

    def post(self, request):
        serialized_user = UserSerializer(data=request.data)
        if serialized_user.is_valid():
            serialized_user.save()
            user = User.objects.get(username=request.data['username'])
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh), 
                "access": str(refresh.access_token)
            })
        return Response(serialized_user.errors, status=HTTP_400_BAD_REQUEST)
    
    
