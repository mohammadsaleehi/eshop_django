# Github.com/Rasooll
from django.urls import path
from . import views

urlpatterns = [
    path('request-payment/', views.send_request_payment, name='request_payment'),
    path('verify-payment/', views.verify_payment, name='verify_payment'),
]
