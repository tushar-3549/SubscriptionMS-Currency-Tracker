from django.contrib import admin
from django.urls import path, include
from subscriptions.views import subscription_list

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('subscriptions.urls')),
    path('subscriptions/', subscription_list, name='subscription_list'),
]
