from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from accounts.views import EmailTokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/login/', EmailTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]