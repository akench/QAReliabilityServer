from django.urls import path
from . import views

urlpatterns = [
	path('generate_report', views.generate_report, name='generate_report')
]