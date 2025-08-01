from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('subscribe/', views.subscribe),
    path('subscriptions/', views.user_subscriptions),
    path('cancel/', views.cancel_subscription),
    path('exchange-rate/', views.exchange_rate),

    # JWT Token endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]