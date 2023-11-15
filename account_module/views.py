from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string
from django.views import View

from utils.email_service import send_email
from .forms import RegisterForm, LoginForm, ForgetPasswordForm
from .models import User
from site_module.models import SiteSetting


# Create your views here.

class RegisterView(View):
	form_class = RegisterForm
	template_name = 'account_module/register.html'

	def get(self, request):
		register_form = self.form_class
		context = {'register_form': register_form}
		return render(request, self.template_name, context)

	def post(self, request):
		register_form = self.form_class(request.POST)
		if register_form.is_valid():
			user_user_name = register_form.cleaned_data.get('user_name')
			user_email = register_form.cleaned_data.get('email')
			user_password = register_form.cleaned_data.get('password')
			user1 = User.objects.filter(email=user_email).exists()
			if user1:
				register_form.add_error('email', 'این ایمیل قبلا ثبت نام کرده است.')
			user = User.objects.filter(username__exact=user_user_name).exists()
			if user:
				register_form.add_error('user_name', 'این نام کاربری قبلا ثبت نام کرده است.')
			elif not user and not user1:
				now_user = User(
					username=user_user_name,
					email=user_email,
					email_active_code=get_random_string(72),
					is_active=False,
				)
				now_user.set_password(user_password)
				now_user.save()
				site_url = SiteSetting.objects.filter(is_main_setting=True).only('site_url').first().site_url
				send_email('فعالسازی حساب کاربری', now_user.email, {'user': now_user, 'site_url': site_url}, 'emails/activate_account.html')
				messages.success(
					request,
					'یک ایمیل به حساب کاربری شما ارسال شد که میتوانید با مراجعه به آن اکانت خود را فعال کنید',
					extra_tags='info'
				)
				return redirect('account:login_page')
		context = {'register_form': register_form}
		return render(request, self.template_name, context)


class LoginView(View):
	form_class = LoginForm
	template_name = 'account_module/login.html'

	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			messages.error(
				request,
				'شما لاگین کرده اول باید از حساب خود خارج شوید تا دوباره بتوانید لاگین کنید.',
				'danger'
			)
			return redirect('home_page')
		return super().dispatch(request, *args, **kwargs)

	def get(self, request):
		form = self.form_class
		next_page = request.GET.get('next')
		request.session['next_page'] = next_page
		return render(request, self.template_name, {'login_form': form})

	def post(self, request):
		login_form = self.form_class(request.POST)
		if login_form.is_valid():
			user_email_username = login_form.cleaned_data.get('email_or_username')
			if '@' in user_email_username:
				user = User.objects.filter(email__iexact=user_email_username).first()
				if not user:
					user = User.objects.filter(username__exact=user_email_username).first()
			else:
				user = User.objects.filter(username__exact=user_email_username).first()
			user_password = login_form.cleaned_data.get('password')
			if user is not None:
				if user.is_active:
					user_password_check = user.check_password(user_password)
					if user_password_check:
						login(request, user)
						next_page = request.session.get('next_page')
						if next_page:
							return redirect(next_page)
						return redirect('home_page')
					else:
						login_form.add_error(
							'email_or_username',
							'ایمیل یا نام کاربری یا کلمه عبور اشتباه است. به بزرگی/کوچیکی حروف نام کاربری توجه کنید'
						)
				else:
					login_form.add_error(
						'email_or_username',
						'حساب کاربری شما فعال نشده است برای فعالسازی به ایمیلی که به ایمیل شما ارسال شده مراجعه کنید.'
					)
			else:
				login_form.add_error('email_or_username', 'کاربری با مشخصات وارد شده یافت نشد.')
		return render(request, self.template_name, {'login_form': login_form})


class ActivateAccountView(View):
	def get(self, request, email_active_code):
		# user = get_object_or_404(User, email_active_code=email_active_code)
		user = User.objects.filter(email_active_code__exact=email_active_code).first()
		if user is not None:
			if not user.is_active:
				user.is_active = True
				user.email_active_code = get_random_string(72)
				user.save()
				messages.success(request, 'اکانت شما با موفقیت فعال شد', extra_tags='success')
				return redirect('account:login_page')
			else:
				messages.info(request, 'اکانت شما فعال شده است', extra_tags='info')
		raise Http404


class ForgotPasswordView(View):
	form_class = ForgetPasswordForm
	template_name = 'account_module/forget_password.html'

	def get(self, request):
		return render(request, self.template_name, {'forget_pass_form': self.form_class})

	def post(self, request):
		forget_pass_form = self.form_class(request.POST)
		if forget_pass_form.is_valid():
			user_email = forget_pass_form.cleaned_data.get('email')
			user = User.objects.filter(email__iexact=user_email, is_active=True).first()
			if user is not None:
				site_url = SiteSetting.objects.filter(is_main_setting=True).only('site_url').first().site_url
				send_email('بازیابی کلمه عبور', user_email, {'user': user, 'site_url': site_url},
						   'emails/forgot_password.html')
				messages.warning(request,
								 'یک ایمیل به ایمیل حساب شما ارسال شد و با مراجعه به آن میتوانید رمز خود را تغغیر دهید',
								 extra_tags='danger')
				return redirect('home_page')
			else:
				forget_pass_form.add_error('email', 'حساب کاربری به این ایمیل وجود ندارد.')
		return render(request, self.template_name, {'forget_pass_form': forget_pass_form})


class ResetPassView(View):
	form_class = RegisterForm
	template_name = 'account_module/reset_password.html'

	def get(self, request, active_code):
		user = User.objects.filter(email_active_code__iexact=active_code).first()
		if user is None:
			return redirect('account:login_page')
		context = {
			'user': user,
			'reset_pass_form': self.form_class
		}
		return render(request, self.template_name, context)

	def post(self, request, active_code):
		reset_pass_form = self.form_class(request.POST)
		user = User.objects.filter(email_active_code__iexact=active_code).first()
		if reset_pass_form.is_valid():
			if user is None:
				return redirect('account:login_page')
			user.set_password(reset_pass_form.cleaned_data['password'])
			user.email_active_code = get_random_string(72)
			user.is_active = True
			user.save()
			return redirect('account:login_page')

		context = {
			'reset_pass_form': reset_pass_form
		}
		return render(request, self.template_name, context)


class LogoutView(LoginRequiredMixin, View):
	def get(self, request):
		logout(request)
		return redirect('account:login_page')
