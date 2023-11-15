from django.shortcuts import redirect


def permission_checker_decorator_factory(data=None):
	def permission_checker_decorator(func):
		def wrapper(request, *args, **kwargs):
			if request.user.is_authenticated and request.user.is_superuser and request.user.is_active:
				return func(request, *args, **kwargs)
			else:
				return redirect('account:login_page')

		return wrapper

	return permission_checker_decorator
