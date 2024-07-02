from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.views import APIView




from rest_framework import generics, permissions, status
from rest_framework.permissions import AllowAny
from .models import Taom, Buyurtma
from .serializers import TaomSerializer, BuyurtmaSerializer

from .serializers import UserSerializer, UserDetailSerializer,RatingSerializer

User = get_user_model()

class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

class ObtainTokenPairWithUserView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        user = User.objects.filter(username=request.data.get('username')).first()
        if user and user.check_password(request.data.get('password')):
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Invalid Credentials'}, status=400)


# Profile
class UserDetail(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user



# Menyu
class TaomListAPIView(generics.ListAPIView):
    queryset = Taom.objects.all()
    serializer_class = TaomSerializer
    permission_classes = [permissions.AllowAny]


# Buyurtma qilish
class BuyurtmaCreateAPIView(generics.CreateAPIView):
    queryset = Buyurtma.objects.all()
    serializer_class = BuyurtmaSerializer
    permission_classes = [permissions.IsAuthenticated]



#Buyurtmalar royhatini ko'rish
class BuyurtmaListAPiView(generics.ListAPIView):
    queryset = Buyurtma.objects.all()
    serializer_class = BuyurtmaSerializer
    permission_classes = [permissions.IsAuthenticated]

#Buyurtmani tasdiqlash

@api_view(['POST'])
def buyurtma_tasdiqlash(request):
    serializer = BuyurtmaSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                'message': 'Sizning buyurtmangiz 20-30 daqiqada yetkazib beriladi',
                'data': serializer.data
            },
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def accept_order(request,order_id):
    try:
        buyurtma = Buyurtma.objects.filter(id=order_id)
        buyurtma.status = 'accepted'
        buyurtma.save()
        return Response({'message': 'Buyurtma qabul qilindi'}, status=status.HTTP_200_OK)
    except Buyurtma.DoesNotExist:
        return Response({'error': 'Buyurtma topilmadi'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def rate_order(request):
    serializer = RatingSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Reytingingiz uchun rahmat'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# Savat ko'rish
class SavatchaListAPIView(generics.ListAPIView):
    queryset = Buyurtma.objects.all()
    serializer_class = BuyurtmaSerializer
    permission_classes = [permissions.IsAuthenticated]


#Savatni tahrirlash
class SavatRetrieweUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Buyurtma.objects.all()
    serializer_class = BuyurtmaSerializer
    permission_classes = [permissions.IsAuthenticated]


