from django.urls import path
from . import views

app_name = 'patient'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('take-test/', views.take_test, name='take-test'),
    path('test/', views.go_to_test_page, name='go-to-test-page'),
    path('appointment/', views.appointment, name='appointment'),
    path('approved-appointment-list/', views.approved_appointments, name='approved_appointments'),
    path('pending-appointment-list/', views.pending_appointments, name='pending_appointments'),
    path('verify-payment/', views.verify_payment, name='verify_payment')
]