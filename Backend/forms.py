from django import forms
from .models import Appointment
from .models import Prescription
from .models import Backend_message

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['name', 'email', 'phone', 'date', 'time', 'doctor', 'message', 'is_message']
        widgets = {
            'is_message': forms.HiddenInput()  # Keep it hidden if necessary
        }


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ["user_name", "phone","email", "address", "prescription_file", "additional_medicines"]

class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = Backend_message
        fields = ['name', 'email', 'phone', 'message'] 