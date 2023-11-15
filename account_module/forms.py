from django import forms
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core import validators
from django.core.exceptions import ValidationError
import string


class RegisterForm(forms.Form):
    user_name = forms.CharField(
        label='نام کاربری',
        widget=forms.TextInput(
            attrs={
                'placeholder': "User Name...",
                'dir': "ltr"
            }
        ),
        validators=[
            UnicodeUsernameValidator()
        ],
        error_messages={
            'required': 'لطفا نام کاربری خود را وارد کنید',
            'max_length': 'نام کاربری نمی تواند بیشتر از 100 کارکتر باشد'

        },
        help_text='الزامی. 150 کاراکتر یا کمتر. فقط شامل حروف، اعداد، و علامات . یا _'
    )
    email = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput(
            attrs={
                'placeholder': "Email...",
                'dir': "ltr"
            }
        ),
        validators=[
            validators.MaxLengthValidator(100),
            validators.EmailValidator,

        ],

    )
    password = forms.CharField(
        label='کلمه عبور',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': "Password",
                "dir": "ltr"
            }
        ),
        validators=[
            validators.MaxLengthValidator(100),
            validators.MinLengthValidator(8)
        ],
    )
    confirm_password = forms.CharField(
        label='تکرار کلمه عبور',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': "Confirm Password",
                "dir": "ltr"
            }
        ),
        validators=[
            validators.MaxLengthValidator(100),
            validators.MinLengthValidator(8)
        ],
    )

    def clean_user_name(self):
        username = self.cleaned_data['user_name']
        v = ""
        for char in username:
            if char in (string.ascii_letters + "123456789._"):
                v += char
        if len(v) == len(username):
            return username
        raise ValidationError(message='نام کاربری فقط شامل حروف انگلیسی و اعداد و . یا _ است')

    def clean_confirm_password(self):
        confirm_password = self.cleaned_data['confirm_password']
        password = self.cleaned_data['password']
        if confirm_password == password:
            if not password.isdigit():
                return confirm_password
            else:
                raise ValidationError(message='کلمه عبور نمی تواند تمام کارکترها اعداد باشد')
        raise ValidationError(message='کلمه عبور و تکرار کلمه عبور مغایرت دارند.')


class LoginForm(forms.Form):
    email_or_username = forms.CharField(
        max_length=60,
        label='ایمیل یا نام کاربری',
        widget=forms.TextInput(
            attrs={
                'placeholder': "ایمیل یا نام کاربری"
            }
        ),
        validators=[
            validators.MaxLengthValidator(100),

        ]
    )

    password = forms.CharField(
        label='کلمه عبور',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': "رمز عبور"
            }
        ),
        validators=[
            validators.MaxLengthValidator(100),
            validators.MinLengthValidator(8)
        ]
    )


class ForgetPasswordForm(forms.Form):
    email = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput(
            attrs={
                'placeholder': "ایمیل"
            }
        ),
        validators=[
            validators.MaxLengthValidator(100),
            validators.EmailValidator(),
        ],
        error_messages={
            'required': 'لطفا ایمیل خود را وارد کنید',
        }
    )


class ResetPasswordForm(forms.Form):
    password = forms.CharField(
        label='کلمه عبور جدید',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': "رمز عبور جدید"
            }
        ),
        validators=[
            validators.MaxLengthValidator(100),
            validators.MinLengthValidator(8)
        ],
        error_messages={
            'required': 'لطفا رمز عبور جدید خود را وارد کنید',
            'max_length': 'رمز عبور جدید نمی تواند بیشتر از 100 کارکتر باشد'
        }
    )
    confirm_password = forms.CharField(
        label='تکرار کلمه عبور جدید',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': "تکرار رمز عبور جدید"
            }
        ),
        validators=[
            validators.MaxLengthValidator(100),
            validators.MinLengthValidator(8)
        ],
        error_messages={
            'required': 'لطفا تکرار رمز عبور جدید خود را وارد کنید',
            'max_length': 'تکرار رمز عبور جدید نمی تواند بیشتر از 100 کارکتر باشد'
        }
    )

    def clean_confirm_password(self):
        confrim_pass = self.cleaned_data['confirm_password']

        password = self.cleaned_data['password']
        # if password == confrim_pass:
        #     if not password.isdigit():
        #         return confrim_pass
        #     raise ValidationError(message='کلمه عبور نمی تواند همش اعداد باشد')
        # raise ValidationError(message='کلمه عبور و تکرار کلمه عبور مغایرت دارند.')
        if password != confrim_pass:
            raise ValidationError(message='کلمه عبور و تکرار کلمه عبور مغایرت دارند.')
        if password.isdigit():
            raise ValidationError(message='کلمه عبور نمی تواند همش اعداد باشد')
        return confrim_pass

