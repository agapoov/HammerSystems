from django.urls import path

from .views import AuthVerifyCodeView, AuthView, ProfileView

urlpatterns = [
    path('entry/', AuthView.as_view(), name='auth-entry'),
    path('verify/', AuthVerifyCodeView.as_view(), name='auth-verify'),

]
