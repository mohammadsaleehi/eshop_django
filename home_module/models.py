from django.db import models

from account_module.models import User


# Create your models here.
class IPAddress(models.Model):
	ip_address = models.GenericIPAddressField(unique=True, verbose_name='آی پی کاربر')

	# article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='مقاله')
	# user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
	class Meta:
		verbose_name = 'آی پی کاربر'
		verbose_name_plural = 'آی پی کاربران'

	def __str__(self):
		return f'{self.ip_address} --> {self.id}'
