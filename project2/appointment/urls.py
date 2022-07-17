from .views import AppointmentView
from django.urls import path

urlpatterns = [
    path('make_appointment/', AppointmentView.as_view(), name='make_appointment'),
]