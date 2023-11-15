from django import forms
from .models import ContactUs


class ContactUsModelForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ('full_name', 'email', 'title', 'message')
        labels = {
            'title': 'موضوع',
            'message': 'پیام شما'
        }
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام و نام خانوادگی'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'ایمیل'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'موضوع'
            }),
            'message': forms.Textarea(attrs={
                'rows': 8,
                'class': 'form-control',
                'id': 'message',
                'placeholder': 'پیام شما'
            })
        }
        error_messages = {
            'full_name': {
                'required': 'لطفا نام و نام خانوادگی خود را وارد کنید',
                'max_length': 'نام و نام خانوادگی نمی تواند بیشتر از 50 کارکتر باشد'
            },
            'email': {
                'required': 'لطفا ایمیل خود را وارد کنید'
            },
            'title': {
                'required': 'لطفا موضوع خود را وارد کنید',
                'max_length': 'موضوع نمی تواند بیشتر از 50 کارکتر باشد'
            },
            'message': {
                'required': 'لطفا متن پیام خود را وارد کنید',
            }
        }
