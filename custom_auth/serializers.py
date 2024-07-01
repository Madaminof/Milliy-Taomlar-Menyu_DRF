from django.contrib.auth import get_user_model
from rest_framework import serializers, status
from rest_framework.response import Response
from custom_auth.models import Taom, Buyurtma
from rest_framework.decorators import action
from django.db.transaction import atomic


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class TaomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Taom
        fields = ['id', 'nomi', 'tarkibi', 'narxi', 'rasmi']


class BuyurtmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buyurtma
        fields = ['id', 'foydalanuvchi', 'taom', 'quantity', 'buyurtma_sanasi', 'manzil', 'tolov_usuli','likes']
        read_only_fields = ['foydalanuvchi']

    def create(self, validated_data):
        validated_data['foydalanuvchi'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['foydalanuvchi'] = self.context['request'].user
        return super().update(instance, validated_data)

    def delete(self,instance):
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



    @action(detail=True, methods=['GET'])
    def liked(self, request, *args, **kwargs):
        buyurtma = self.get_object()
        with atomic():
            buyurtma.likes += 1
            buyurtma.save()


        return Response({'message': 'Buyurtma liked successfully', 'likes': buyurtma.likes}, status=status.HTTP_200_OK)



