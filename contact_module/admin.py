from django.contrib import admin
from . import models
# Register your models here.
@admin.register(models.ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'title', 'created_data', 'is_read_by_admin']
    list_filter = ['is_read_by_admin']
    list_editable = ['is_read_by_admin']
    date_hierarchy = 'created_data'
