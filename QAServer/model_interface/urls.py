from django.urls import path
from . import views

urlpatterns = [
	path('create_report', views.generate_report, name='create_report'),
	path('collect_data', views.collect_data, name='collect_data')
]