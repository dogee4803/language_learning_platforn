from django.urls import path
from .views import CustomersView, CustomerDetailView

urlpatterns = [
    path('customers/', CustomersView.as_view(), name='customers-list'),
    path('customers/<int:pk>/', CustomerDetailView.as_view(), name='customer-detail'),
]
