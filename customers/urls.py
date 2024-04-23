from django.urls import path
from customers.views import CreateCustomerView, LoginView

urlpatterns = [
    path("login/", LoginView.as_view()),
    path("register/", CreateCustomerView.as_view()),
]