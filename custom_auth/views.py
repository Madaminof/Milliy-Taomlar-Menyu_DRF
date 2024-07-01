from nltk import app
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from flask import Flask, request, jsonify, app



from rest_framework import generics, permissions
from rest_framework.permissions import AllowAny
from .models import Taom, Buyurtma
from .serializers import TaomSerializer, BuyurtmaSerializer

from .serializers import UserSerializer, UserDetailSerializer

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

    @app.route('/submit_order', methods=['POST'])
    def submit_order():
        data = request.get_json()
        orders.append(data)
        estimated_delivery_time = estimate_delivery_time(data)
        return jsonify({'message': 'Buyurtma tasdiqlandi va qabul qilindi',
                        'estimated_delivery_time': estimated_delivery_time}), 200

    def estimate_delivery_time(order_data):
        # Bu funksiya orqali yetkazib berish vaqti taxmin qilingan bo'lishi kerak
        return "2 kun ichida"




class BuyurtmaListAPiView(generics.ListAPIView):
    queryset = Buyurtma.objects.all()
    serializer_class = BuyurtmaSerializer
    permission_classes = [permissions.IsAuthenticated]


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

app = Flask(__name__)

# Bu yerda buyurtmalar ro'yxati saqlanadi
orders = []

# 6. Buyurtmani tasdiqlash va jo'natish
@app.route('/submit_order', methods=['POST'])
def submit_order():
    data = request.get_json()
    orders.append(data)
    estimated_delivery_time = estimate_delivery_time(data)
    return jsonify({'message': 'Buyurtma tasdiqlandi va qabul qilindi', 'estimated_delivery_time': estimated_delivery_time}), 200

def estimate_delivery_time(order_data):
    # Bu funksiya orqali yetkazib berish vaqti taxmin qilingan bo'lishi kerak
    return "2 kun ichida"

# 7. Buyurtmani qabul qilish va baholash
@app.route('/receive_order', methods=['POST'])
def receive_order():
    data = request.get_json()
    # Bu erda buyurtmani qabul qilib, taom sifati va xizmat darajasini baholaymiz
    quality_rating = data.get('quality_rating')
    service_rating = data.get('service_rating')
    return jsonify({'message': 'Buyurtma qabul qilindi va baholandi', 'quality_rating': quality_rating, 'service_rating': service_rating}), 200

# 8. Chiqish
@app.route('/exit', methods=['GET'])
def exit_program():
    return jsonify({'message': 'Dasturdan muvaffaqiyatli chiqildi'}), 200



