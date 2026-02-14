"""
URL configuration for Backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Backend import views
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('appointments/', views.appointment, name='appointments'),
    path('cancel-appointment/', views.cancel_appointment, name='cancel_appointment'),
    path('contact/', views.contact, name='contact'),
    path("upload-prescription/", views.upload_prescription, name="upload_prescription"),
    path('', include('chatbot.urls')),
    path('download_report/<int:report_id>/', views.download_report, name='download_report'),
    path('lab_reports/', views.lab_reports, name='lab_reports')
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
