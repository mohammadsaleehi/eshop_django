from django.contrib import admin
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.contrib.auth.admin import UserAdmin
from .models import User


# admin.site.register(User, UserAdmin)
@admin.register(User)
class UserAdmin(UserAdmin):
	list_display = ['id', 'username', 'email', 'first_name', 'last_name', 'is_superuser', 'is_active', 'is_special_user']
	list_filter = ("is_staff", "is_superuser", "is_active", "groups")
	search_fields = ['username', 'email']
	fieldsets = (
		(None, {"fields": ("username", "password")}),
		("اطلاعات شخصی", {"fields": ("first_name", "last_name", "email", "avatar", "email_active_code")}),
		(
			"اجازه‌ها",
			{
				"fields": (
					"is_active",
					"is_staff",
					"is_superuser",
					"groups",
					"user_permissions",
				),
			},
		),
		("تاریخ‌های مهم", {"fields": ("special_user", "last_login", "date_joined")}),
		("فیلد های نوشتاری", {'fields': ("about_user", "address")})
	)
	add_fieldsets = (
		(
			None,
			{
				"classes": ("wide",),
				"fields": ("username", 'email', "password1", "password2"),
			},
		),
	)
	# ordering = ('-id',)
	
	# def has_add_permission(self, request):
	# 	return False