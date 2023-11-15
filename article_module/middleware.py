from django.db import connection

from home_module.models import IPAddress
from utils.http_service import get_client_ip


class SaveIPAddress:
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		ip_user = get_client_ip(request)
		ip_address, b = IPAddress.objects.get_or_create(ip_address=ip_user)
		request.user.ip_address = ip_address
		response = self.get_response(request)
		return response