from django import forms
from django.core import validators
from django.core.exceptions import ValidationError

from account_module.models import User


class EditProfileModelForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'avatar', 'about_user', 'address')
		labels = {
			'first_name': 'نام',
			'last_name': 'نام خانوادگی',
			'avatar': 'تصویر پروفایل',
			'about_user': 'درباره من',
			'address': 'آدرس'
		}
		widgets = {
			'first_name': forms.TextInput(attrs={
				'class': 'form-control',
				'placeholder': 'نام'
			}),
			'last_name': forms.TextInput(attrs={
				'class': 'form-control',
				'placeholder': 'نام خانوادگی'
			}),
			'avatar': forms.FileInput(attrs={
				'class': 'form-control'
			}),
			'about_user': forms.Textarea(attrs={
				'rows': 6,
				'class': 'form-control',
				'placeholder': 'درباره من'
			}),
			'address': forms.Textarea(attrs={
				'rows': 6,
				'class': 'form-control',
				'placeholder': 'آدرس'
			})
		}
		error_messages = {
			'first_name': {
				'required': 'لطفا نام خود را وارد کنید',
				'max_length': 'نام نمی تواند بیشتر از 50 کارکتر باشد'
			},
			'last_name': {
				'required': 'لطفا نام خانوادگی خود را وارد کنید',
				'max_length': 'نام خانوادگی نمی تواند بیشتر از 50 کارکتر باشد'
			},
			'avatar': {
				'required': 'لطفا تصویر پروفایل خود را وارد کنید',
			},
			'about_user': {
				'required': 'لطفا درباره من را وارد کنید',
			},
		}


class ChangePasswordForm(forms.Form):
	current_password = forms.CharField(
		label='کلمه عبور',
		widget=forms.PasswordInput(
			attrs={
				'class': 'form-control',
				'placeholder': "کلمه عبور"
			}
		),
		validators=[
			validators.MaxLengthValidator(100)
		]
	)
	now_password = forms.CharField(
		label='کلمه عبور جدید',
		widget=forms.PasswordInput(
			attrs={
				'class': 'form-control',
				'placeholder': "کلمه عبور جدید"
			}
		),
		validators=[
			validators.MaxLengthValidator(100),
			validators.MinLengthValidator(8)
		],
		error_messages={
			'required': "لطفا کلمه عبور جدید را وارد کنید",
			'min_length': "کلمه عبور نمی تواند از هشت کارکتر کمتر باشد"
		}
	)
	confirm_password = forms.CharField(
		label='تکرار کلمه عبور جدید',
		widget=forms.PasswordInput(
			attrs={
				'class': 'form-control',
				'placeholder': "تکرار کلمه عبور جدید"
			}
		)
	)

	def clean_confirm_password(self):
		confirm_password = self.cleaned_data['confirm_password']
		password = self.cleaned_data['now_password']
		if confirm_password == password:
			if not password.isdigit():
				return confirm_password
			else:
				raise ValidationError(message='کلمه عبور نباید همش اعداد باشد')
		else:
			raise ValidationError(message='کلمه عبور و تکرار کلمه عبور مغایرت دارند.')
