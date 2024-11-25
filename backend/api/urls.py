from django.urls import path
from .views import ExampleView, CustomersView

urlpatterns = [
    path('example/', ExampleView.as_view(), name='example'),
    path('customers/', CustomersView.as_view(), name='customers-list'),
]
