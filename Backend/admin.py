from django.contrib import admin
from .models import Prescription
from .models import Appointment
from .models import Backend_message

from django.contrib import admin
from .models import Prescription, Appointment, Backend_message

from django.utils.timezone import now

from .models import LabReport

admin.site.register(LabReport)

# Customize the admin site title
admin.site.site_header = "Matoshree Hospital Admin"  # Custom name on the login page
admin.site.site_title = "Matoshree Admin Portal"      # Title in the browser tab
admin.site.index_title = "Welcome to Matoshree Hospital Admin"  # Title on the admin index page


@admin.register(Backend_message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "created_at")  # Added phone field for better clarity
    search_fields = ("name", "email", "phone")
    ordering = ("-created_at",)
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "doctor", "date", "time", "status", "is_message")
    list_filter = ("doctor", "date", "status", "is_message")
    search_fields = ("name", "phone", "doctor")
    ordering = ("-date", "-time")
    actions = ['cancel_appointments']
    
    # Makes the status column editable directly from the list view
    list_editable = ('status',)
    
    # Shows a cancel button for each appointment in the list
    def cancel_appointments(self, request, queryset):
        updated = queryset.update(status='Canceled', cancelled_at=now())
        self.message_user(request, f"{updated} appointment(s) were successfully marked as canceled.")
    cancel_appointments.short_description = "Cancel selected appointments"
    
    # Shows only non-canceled appointments by default
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.GET.get('status__exact') and not request.GET.get('all'):
            return qs.exclude(status='Canceled')
        return qs
    
    # Add a view to see all appointments including canceled ones
    def changelist_view(self, request, extra_context=None):
        if 'all' in request.GET:
            self.list_filter = ("doctor", "date", "is_message")
        else:
            self.list_filter = ("doctor", "date", "is_message", "status")
        return super().changelist_view(request, extra_context=extra_context)

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ("user_name", "phone","email", "status", "uploaded_at")
    list_filter = ("status", "uploaded_at")
    search_fields = ("user_name", "phone")
    ordering = ("-uploaded_at",)

