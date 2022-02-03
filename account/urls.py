from django.urls import path
from .views import RegistrationView, LoginView, ActivationView, LogOutView

urlpatterns = [
    path('signup/', RegistrationView.as_view()),
    path('login/', LoginView.as_view()),
    path('activate/', ActivationView.as_view()),
    path('logout/', LogOutView.as_view()),
]