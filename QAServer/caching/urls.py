from django.urls import path
from . import views

urlpatterns = [
	path('get_cached_report/<url>', views.get_report, name='get_report')
]