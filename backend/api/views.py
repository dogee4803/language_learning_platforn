from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Customer
from .serializers import CustomerSerializer

class ExampleView(APIView):
    def get(self, request):
        return Response({"message": "Hello from Django API!"})
    
class CustomersView(APIView):
    def get(self, request):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)
