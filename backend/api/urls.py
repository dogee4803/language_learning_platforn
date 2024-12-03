from django.urls import path
from .views.customers import CustomersView, CustomerDetailView
from .views.financial_report import financial_report
from .views.auth import login, logout

urlpatterns = [
    # Auth endpoints
    path('auth/login/', login, name='login'),
    path('auth/logout/', logout, name='logout'),
    
    # Existing endpoints
    path('customers/', CustomersView.as_view(), name='customers-list'),
    path('customers/<int:pk>/', CustomerDetailView.as_view(), name='customer-detail'),
    path('financial-report/', financial_report, name='financial-report'),
]
