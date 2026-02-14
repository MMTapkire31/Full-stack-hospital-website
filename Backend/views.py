from django.shortcuts import render, redirect
from .models import Appointment
from django.http import FileResponse, Http404
from django.contrib import messages
from django.core.mail import EmailMessage
import requests
from django.db.models import Q
from django.core.mail import send_mail
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime
from django.shortcuts import get_object_or_404
from datetime import datetime
from urllib.parse import quote
from django.http import HttpResponse
from django.utils import timezone
from django.contrib import messages
from .forms import ContactMessageForm
from datetime import date, time
from .forms import PrescriptionForm
from .models import Prescription
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from .models import Backend_message
from django.http import HttpResponse, FileResponse
from .models import LabReport
from django.core.mail import send_mail
from django.conf import settings

def home(request):
    return render(request, "index.html")

def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, "contact.html")

from django.utils import timezone
from datetime import datetime, time
from django.core.mail import send_mail
from django.contrib import messages

def appointment(request):
    if request.method == "POST":
        # Get form data
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        date_str = request.POST.get('date', '')
        time_str = request.POST.get('time', '')
        doctor = request.POST.get('doctor', '').strip()
        message = request.POST.get('message', '').strip()

        # Basic validation
        if not all([name, email, phone, date_str, time_str, doctor]):
            messages.error(request, "Please fill in all required fields.")
            return render(request, 'appointment.html')

        # Validate date
        try:
            appointment_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            if appointment_date < timezone.now().date():
                messages.error(request, "Appointment date cannot be in the past.")
                return render(request, 'appointment.html')
        except ValueError:
            messages.error(request, "Invalid date format. Please use YYYY-MM-DD.")
            return render(request, 'appointment.html')

        # Validate time
        try:
            hour, minute = map(int, time_str.split(':'))
            appointment_time = time(hour, minute)
            
            # Check time is between 9 AM and 8 PM
            if not (9 <= hour < 20):
                messages.error(request, "Appointments are only available between 9 AM and 8 PM.")
                return render(request, 'appointment.html')
        except (ValueError, AttributeError):
            messages.error(request, "Invalid time format. Please use HH:MM.")
            return render(request, 'appointment.html')

        # Check for existing appointments
        if Appointment.objects.filter(date=appointment_date, time=time_str, doctor=doctor).exists():
            messages.error(request, "This time slot is already booked with the selected doctor. Please choose another time or doctor.")
            return render(request, 'appointment.html')

        # Save appointment to database
        try:
            new_appointment = Appointment(
                name=name,
                email=email,
                phone=phone,
                date=appointment_date,
                time=time_str,
                doctor=doctor,
                message=message
            )
            new_appointment.save()
        except Exception as e:
            messages.error(request, f"Error saving appointment: {str(e)}")
            return render(request, 'appointment.html')

        # Send confirmation email
        subject = "✅ Appointment Confirmation – Matoshree Hospital"
        body = (
            f"Dear {name},\n\n"
            f"🎉 Your appointment has been booked successfully!\n\n"
            f"📋 **Details:**\n"
            f"    👨‍⚕️ Doctor: {doctor}\n"
            f"    🗓️ Date: {appointment_date.strftime('%B %d, %Y')}\n"
            f"    ⏰ Time: {time_str}\n"
            f"    📞 Phone: {phone}\n"
            f"    💬 Message: {message or 'None'}\n\n"
            F"⏲️Please arrive 15 minutes before your scheduled time\n\n"
            f"🙏 Thank you for choosing Matoshree Hospital.\n"
            f"🏥 We look forward to serving you with care and compassion.\n\n"
            F"❌If you want to cancel the appointment then visit our website page.\n\n"
            f"📍 Location: [Shivratna Nagar, Gopalpur, Pandharpur-413304]\n"
            f"📞 Contact: [+91 9822 353 125.]\n\n"
            f"💙 Best regards,\n"
            f"🌿 Matoshree Hospital Team ✨"
        )

        try:
            send_mail(
                subject,
                body,
                'matoshreehospital82@gmail.com',  # Use a dedicated email
                [email],
                fail_silently=False
            )
            messages.success(request, " ")
        except Exception as e:
            # Appointment was saved but email failed
            messages.warning(request, f"Appointment booked but we couldn't send confirmation email. Error: {str(e)}")

        return redirect('appointment_success')  # Redirect to a success page
    

    return render(request, "appointment.html")
def cancel_appointment(request):
    if request.method == "POST":
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        appointment_id = request.POST.get('appointment_id', '').strip()
        reason = request.POST.get('reason', '').strip()

        # Validate required fields
        if not email or not phone:
            return JsonResponse({
                'success': False,
                'message': 'Email and phone number are required.'
            })

        # Find the appointment
        try:
            # Try to find by ID first if provided
            if appointment_id:
                appointment = Appointment.objects.get(id=appointment_id, email=email, phone=phone)
            else:
                # Otherwise find by email and phone
                appointments = Appointment.objects.filter(email=email, phone=phone).order_by('-date', '-time')
                
                if not appointments:
                    return JsonResponse({
                        'success': False,
                        'message': 'No appointments found with the provided information.'
                    })
                
                # Get the most recent appointment
                appointment = appointments.first()

            # Check if appointment is in the past
            current_datetime = timezone.now()
            
            # Fix for the datetime parsing issue
            # First convert the time to string and handle potential formats
            time_str = str(appointment.time)
            
            # Remove seconds if present to match the format string
            if len(time_str.split(':')) > 2:
                # If time has seconds (HH:MM:SS), remove the seconds part
                time_str = ':'.join(time_str.split(':')[:2])
            
            # Create a clean datetime string
            appointment_datetime_str = f"{appointment.date} {time_str}"
            
            try:
                # Try parsing with the standard format
                appointment_datetime = datetime.strptime(appointment_datetime_str, '%Y-%m-%d %H:%M')
            except ValueError:
                # If that fails, try an alternative format
                try:
                    appointment_datetime = datetime.strptime(appointment_datetime_str, '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    # If all parsing attempts fail, report the error
                    return JsonResponse({
                        'success': False,
                        'message': f'Error processing appointment time. Please contact support.'
                    })
            
            # Make the datetime timezone aware
            appointment_datetime = timezone.make_aware(appointment_datetime)
            
            if appointment_datetime < current_datetime:
                return JsonResponse({
                    'success': False,
                    'message': 'Cannot cancel a past appointment.'
                })
            
            # Check if appointment is within 4 hours
            time_difference = appointment_datetime - current_datetime
            if time_difference.total_seconds() < 14400:  # 4 hours = 14400 seconds
                return JsonResponse({
                    'success': False,
                    'message': 'Appointments must be cancelled at least 4 hours in advance.'
                })

            # Send cancellation email
            subject = "Appointment Cancellation Confirmation – Matoshree Hospital"
            body = (
                f"Dear {appointment.name},\n\n"
                f"Your appointment scheduled for {appointment.date.strftime('%B %d, %Y')} at {appointment.time} "
                f"with {appointment.doctor} has been successfully cancelled.\n\n"
                f"Cancellation reason: {reason or 'Not provided'}\n\n"
                f"If you wish to reschedule, please visit our website or call our helpline at +91 9822 353 125.\n\n"
                f"Thank you for informing us in advance.\n\n"
                f"💙 Best regards,\n"
                f"🌿 Matoshree Hospital Team ✨"
            )

            # Send email
            try:
                send_mail(
                    subject,
                    body,
                    'matoshreehospital@gmail.com',
                    [email],
                    fail_silently=False
                )
            except Exception as e:
                # Log email error but continue with cancellation
                print(f"Error sending cancellation email: {str(e)}")

            # Record the cancellation reason if provided
            appointment.status = 'Cancelled'
            appointment.cancellation_reason = reason
            appointment.cancelled_at = timezone.now()
            appointment.save()

            return JsonResponse({
                'success': True,
                'message': 'Your appointment has been successfully cancelled. A confirmation email has been sent.'
            })

        except Appointment.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'No matching appointment found with the provided details.'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'An error occurred: {str(e)}'
            })

    # If not POST request
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method.'
    })

def services(request):
    return render(request, "services.html")


def upload_prescription(request):
    if request.method == "POST":
        form = PrescriptionForm(request.POST, request.FILES)
        
        if form.is_valid():
            prescription = form.save()

            # Send email after uploading prescription
            patient_name = prescription.user_name  # Assuming you have a 'patient_name' field
            patient_email = prescription.email  # Assuming you have an 'email' field
            hospital_contact = "123-456-7890"  # Replace with your hospital's contact number

            subject = "✅ Prescription Upload Confirmation – Matoshree Hospital"
            body = (
                f"Dear {patient_name},\n\n"
                f"🩺 Your prescription has been successfully uploaded.\n\n"

                f"📞 If you have any questions, feel free to contact us:\n"
                f"    📱 **Contact:** {hospital_contact}\n\n"
                f"🙏 Thank you for trusting Matoshree Hospital with your care.\n"
                f"🏥 We look forward to serving you.\n\n"
                f"💙 Best regards,\n"
                f"🌿 Matoshree Hospital Team ✨"
            )

            try:
                send_mail(
                    subject,
                    body,
                    'your_email@gmail.com',  # Replace with your hospital's email
                    [patient_email],
                    fail_silently=False,
                )
                messages.success(request, "Prescription uploaded and email sent successfully!")
            except Exception as e:
                messages.error(request, f"Prescription uploaded, but email failed: {str(e)}")

            return redirect("upload_prescription")  # Redirect to the same page to show the message

    else:
        form = PrescriptionForm()

    return render(request, "prescription_upload.html", {"form": form})


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        message_text = request.POST.get("message")

        if name and email and message_text:
            # Save the message in the database
            Backend_message.objects.create(name=name, email=email, message=message_text)
            
            # Send an email to the entered email address
            subject = "Feedback Received"
            body = (
                f"Dear {name},\n\n"
                f"🙏 Thank you for your feedback! We have received your message.\n"
                f"🏥 We look forward to serving you.\n\n"
                f"💙 Best regards,\n"
                f"🌿 Matoshree Hospital Team ✨"
            )

            from_email = settings.DEFAULT_FROM_EMAIL
            
            try:
                send_mail(subject, body, from_email, [email])
                messages.success(request, "Your message has been sent successfully!")
            except Exception as e:
                messages.error(request, f"Error sending email: {e}")
        else:
            messages.error(request, "All fields are required.")

        return redirect("contact")  # Redirect to the contact page

    return render(request, "contact.html")



def lab_reports(request):
    reports = None
    searched = False
    
    if request.method == 'POST':
        print("POST data:", request.POST)  # Debug
        searched = True
        patient_id = request.POST.get('patient_id')
        patient_name = request.POST.get('patient_name')
        dob_str = request.POST.get('date_of_birth')  # Changed this line
        
        print(f"Searching for: ID={patient_id}, Name={patient_name}, DOB={dob_str}")  # Debug

        if not all([patient_id, patient_name, dob_str]):
            messages.error(request, "Please fill all required fields.")
            return render(request, 'lab_reports.html', {
                'reports': reports,
                'searched': searched
            })
        
        try:
            # Convert from YYYY-MM-DD (form) to date object
            dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
            print(f"Converted DOB: {dob}")  # Debug
            
            reports = LabReport.objects.filter(
                patient_id=patient_id,
                patient_name__iexact=patient_name,
                dob=dob
            )
            
            print(f"Found {reports.count()} reports")  # Debug
            if not reports.exists():
                messages.info(request, "No reports found matching your criteria.")
                
        except ValueError as e:
            print(f"Date error: {e}")  # Debug
            messages.error(request, "Invalid date format. Please use yyyy-mm-dd format.")
    
    return render(request, 'lab_reports.html', {
        'reports': reports,
        'searched': searched
    })


def download_report(request, report_id):
    report = get_object_or_404(LabReport, id=report_id)
    
    if not report.file:
        raise Http404("No file associated with this report")
    
    # Get absolute file path
    file_path = os.path.join(settings.MEDIA_ROOT, report.file.name)
    
    # Debug output
    print(f"Looking for file at: {file_path}")
    print(f"MEDIA_ROOT: {settings.MEDIA_ROOT}")
    print(f"File name: {report.file.name}")
    
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/octet-stream")
            response['Content-Disposition'] = f'attachment; filename="{quote(os.path.basename(report.file.name))}"'
            return response
    else:
        print(f"File not found at: {file_path}")
        if not os.path.exists(settings.MEDIA_ROOT):
            print(f"MEDIA_ROOT directory doesn't exist!")
        raise Http404(f"File not found at: {file_path}")