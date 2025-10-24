from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

def api_root(request):
    return JsonResponse({
        "message": "Welcome to Recipe Vault API 🚀",
        "auth": {
            "register": "/api/v1/auth/register/",
            "login": "/api/v1/auth/token/",
            "token_refresh": "/api/v1/auth/token/refresh/",
            "google_login": "/api/v1/auth/social/google/",
        },
        "recipes": "/api/v1/recipes/",
        "admin": "/admin/"
    })


urlpatterns = [
    path('', api_root),
    path('admin/', admin.site.urls),
    path('api/v1/', include('recipes.urls')),
    path('api/v1/auth/', include('accounts.urls')),
    path('api/v1/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/auth/social/', include('allauth.socialaccount.urls')),

    # # Optional for registration endpoints
    # path('api/v1/auth/social/registration/', include('dj_rest_auth.registration.urls')),

    # # Optional: needed if using django-allauth’s social account admin
    # path('api/v1/auth/social/accounts/', include('allauth.socialaccount.urls')),
]
