from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('doctors/', views.doctor_list_view, name='doctor_list'),
    path('doctors/add/', views.doctor_create_view, name='doctor_create'),
    path('doctors/<int:pk>/', views.doctor_detail_view, name='doctor_detail'),
    
    path('patients/', views.patient_list_view, name='patient_list'),
    path('patients/add/', views.patient_create_view, name='patient_create'),
    path('patients/<int:pk>/', views.patient_detail_view, name='patient_detail'),
    
    path('appointments/', views.appointment_list_view, name='appointment_list'),
    path('appointments/add/', views.appointment_create_view, name='appointment_create'),
    
    path('reports/', views.report_list_view, name='report_list'),
    path('reports/add/', views.report_create_view, name='report_create'),
    path('reports/export/pdf/', views.export_report_pdf, name='export_report_pdf'),
    path('reports/export/csv/', views.export_data_csv, name='export_data_csv'),
    
    path('departments/', views.department_list_view, name='department_list'),
    path('contacts/', views.contact_list_view, name='contact_list'),
    path('settings/', views.settings_view, name='settings'),
    
    path('search/', views.global_search_view, name='global_search'),
]
