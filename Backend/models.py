from django.db import models
from django.utils.timezone import now
import datetime
 


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
        ('No-Show', 'No-Show'),
    ]
    
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='Scheduled'
    )
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15, default="0000000000")
    date = models.DateField(default=datetime.date.today)  # Correct default for DateField
    time = models.TimeField(blank=True, null=True)
    doctor = models.CharField(max_length=255, default="Dr. Unknown")
    message = models.TextField(blank=True, null=True)
    is_message = models.BooleanField(default=False)  # Add this field
    status = models.CharField(max_length=20, default='Scheduled')
    cancellation_reason = models.TextField(blank=True, null=True)
    cancelled_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Appointment with {self.doctor} on {self.date} at {self.time}"
    

class Prescription(models.Model):
    user_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    email = models.EmailField(max_length=100, null=True, blank=True)
    prescription_file = models.FileField(upload_to="prescriptions/")
    additional_medicines = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[("Pending", "Pending"), ("Approved", "Approved"), ("Delivered", "Delivered")],
        default="Pending",
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_name} - {self.status}"




class Backend_message(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, default="")  # Default empty string
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

  
class LabReport(models.Model):
    patient_id = models.CharField(max_length=20)
    patient_name = models.CharField(max_length=100)
    dob = models.DateField()
    report_title = models.CharField(max_length=150)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)
    doctor = models.CharField(max_length=100)
    file = models.FileField(upload_to='reports/')

    def __str__(self):
        return f"{self.report_title} - {self.patient_name}"

