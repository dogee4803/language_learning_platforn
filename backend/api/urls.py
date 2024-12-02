from django.urls import path
from .views.customers import CustomersView, CustomerDetailView
from .views.financial_report import financial_report

urlpatterns = [
    path('customers/', CustomersView.as_view(), name='customers-list'),
    path('customers/<int:pk>/', CustomerDetailView.as_view(), name='customer-detail'),
    path('financial-report/', financial_report, name='financial-report'),
]
