from django import forms
from .models import Appointment

class AppointmentForm(forms.ModelForm):

    class Meta:
        model = Appointment
        fields = ('name', 'email', 'phone', 'appointment_for', 'preffered_date', 'preffered_time', 'doctor')

    