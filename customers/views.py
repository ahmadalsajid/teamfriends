import random
from django.db.models import Sum
from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db import IntegrityError, transaction
from datetime import datetime, timezone
from rest_framework.permissions import AllowAny
from rest_framework.generics import get_object_or_404, ListAPIView
from rest_framework_simplejwt.views import TokenObtainPairView

from customers.models import Customer
from customers.serializers import CustomerSerializer, LoginViewSerializer


class LoginView(TokenObtainPairView):
    serializer_class = LoginViewSerializer


class CreateCustomerView(APIView):

    def get(self, request):
        _data = request.data
        _customers = Customer.objects.all()
        _customer_serializer = CustomerSerializer(_customers, many=True)
        return Response(
            {
                "data": _customer_serializer.data
            },
            status=status.HTTP_201_CREATED
        )
       
    def post(self, request):
        _data = request.data
        _customer = {
            "name": _data.get("name"),
            "email": _data.get("email"),
            "date_of_birth": _data.get("date_of_birth")
        }

        try:
            with transaction.atomic():
                _new_customer = Customer.objects.create(**_customer)
                _customer_serializer = CustomerSerializer(_new_customer)
                return Response(
                    {
                        "data": _customer_serializer.data
                    },
                    status=status.HTTP_201_CREATED
                )
        except Exception as e:
            return Response(
                {
                    "error": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )
