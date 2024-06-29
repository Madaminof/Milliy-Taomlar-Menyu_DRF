from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.contrib.auth.models import User


class CustomUser(AbstractUser):
    groups = models.ManyToManyField(Group, related_name='custom_user_set')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions_set')


# Asosiy Menyu
class Taom(models.Model):
    nomi = models.CharField(max_length=100)
    tarkibi = models.TextField()
    narxi = models.IntegerField()
    rasmi = models.ImageField(upload_to='taomlar/', null=True, blank=True)

    def __str__(self):
        return f"{self.nomi}-{self.narxi}"


# buyurtma
class Buyurtma(models.Model):
    foydalanuvchi = models.ForeignKey(User, on_delete=models.CASCADE)
    taom = models.ForeignKey(Taom, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    buyurtma_sanasi = models.DateTimeField(auto_now_add=True)
    manzil = models.CharField(max_length=255, blank=True, null=True)
    tolov_usuli = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.foydalanuvchi.id}-{self.foydalanuvchi.username} - {self.taom.nomi}- ({self.quantity} ta)"

