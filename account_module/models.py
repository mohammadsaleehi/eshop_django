from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
	email = models.EmailField(verbose_name="ایمیل", blank=True, null=True, unique=True)
	avatar = models.ImageField(upload_to='images/profile/', verbose_name='تصویر آواتار', default='profile.jpg')
	email_active_code = models.CharField(max_length=100, verbose_name='کد فعالسازی ایمیل', null=True, blank=True)
	about_user = models.TextField(null=True, blank=True, verbose_name='درباره شخص')
	address = models.TextField(null=True, blank=True, verbose_name='آدرس')
	special_user = models.DateTimeField(default=timezone.now, verbose_name='کاربر ویژه تا')

	class Meta:
		ordering = ['-id']
		verbose_name = 'کاربر'
		verbose_name_plural = "کاربر ها"

	def is_special_user(self):
		if self.special_user > timezone.now():
			return True
		else:
			return False

	is_special_user.short_description = "وضعیت کاربری ویژه"
	is_special_user.boolean = True
	is_special_user.admin_order_field = 'special_user'

	def __str__(self):
		if self.get_full_name() != '':
			return self.get_full_name()
		else:
			return self.username
