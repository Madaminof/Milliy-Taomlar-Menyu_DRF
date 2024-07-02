from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import UserCreate, ObtainTokenPairWithUserView, UserDetail, TaomListAPIView, BuyurtmaCreateAPIView, \
    SavatRetrieweUpdateDestroyAPIView, SavatchaListAPIView,BuyurtmaListAPiView,buyurtma_tasdiqlash,accept_order,rate_order

urlpatterns = [
    #auth
    path('api/token/', ObtainTokenPairWithUserView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', UserCreate.as_view(), name='register'),

    #profil
    path('api/profile/', UserDetail.as_view(), name='profile'),

    # menyu va buyurtma va tasdiqlash va qabul qilish va baxolash
    path('api/taomlar/', TaomListAPIView.as_view(), name='taomlar-list'),
    path('api/buyurtma/', BuyurtmaCreateAPIView.as_view(), name='buyurtma-create'),
    path('api/buyurtmalar/<int:id>/', BuyurtmaListAPiView.as_view(), name='buyurtmalar-list'),
    path('api/buyurtma_tasdiqlash',buyurtma_tasdiqlash,name='buyurtma-tasdiqlash'),
    path('buyurtmalar/<int:order_id>/accept/', accept_order, name='accept_order'),
    path('buyurtmalar/rate/', rate_order, name='rate_order'),



    # savatcha
    path('api/savatcha/', SavatchaListAPIView.as_view(), name='savatcha-list'),
    path('api/savatcha-update-delete/<int:pk>/', SavatRetrieweUpdateDestroyAPIView.as_view(), name='savatcha-detail'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

