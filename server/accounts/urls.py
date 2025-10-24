from django.urls import path, include
from .views import RegisterView, LoginView, LogoutView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('google/', include('allauth.socialaccount.providers.google.urls')),
]

