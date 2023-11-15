from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import JsonResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView

from account_module.models import User
from order_module.models import Order, OrderDetail
from user_panel_module.forms import EditProfileModelForm, ChangePasswordForm


# Create your views here.
@login_required()
def user_panel_dashboard_page(request):
	return render(
		request,
		'user_panel_module/user_panel_dashboard_page.html',
		{'user': request.user}
	)


@method_decorator(login_required(), name='dispatch')
class EditUserProfilePage(View):
	form_class = EditProfileModelForm
	template_name = 'user_panel_module/edit_profile_page.html'

	def get(self, request):
		current_user = User.objects.get(id=request.user.id)
		edit_form = self.form_class(instance=current_user)
		context = {
			'form': edit_form,
			'current_user': current_user
		}
		return render(request, self.template_name, context)

	def post(self, request):
		current_user = User.objects.get(id=request.user.id)
		edit_form = self.form_class(request.POST, request.FILES, instance=current_user)
		if edit_form.is_valid():
			edit_form.save()
		context = {
			'form': edit_form,
			'current_user': current_user
		}
		return render(request, self.template_name, context)


@method_decorator(login_required(), name='dispatch')
class ChangePasswordPage(View):
	form_class = ChangePasswordForm
	template_name = 'user_panel_module/change_password_page.html'

	def get(self, request):
		return render(request, self.template_name, {'form': self.form_class})

	def post(self, request):
		form = self.form_class(request.POST)
		if form.is_valid():
			current_user = get_object_or_404(User, id=request.user.id)
			if current_user.check_password(form.cleaned_data.get('current_password')):
				current_user.set_password(form.cleaned_data.get('now_password'))
				current_user.save()
				logout(request)
				return redirect('account:login_page')
			else:
				form.add_error('current_password', 'کلمه عبور اشتباه است')
		context = {
			'form': form
		}
		return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class MyShopping(ListView):
	model = Order
	template_name = 'user_panel_module/user_shoppings.html'
	paginate_by = 7

	def get_queryset(self):
		queryset = super().get_queryset()
		queryset = queryset.filter(user_id=self.request.user.id, is_paid=True) \
			.prefetch_related('orderdetail_set')
		return queryset


@login_required
def user_panel_menu_component(request):
	return render(request, 'user_panel_module/components/user_panel_menu_component.html')


@login_required
def user_basket(request):
	user_open_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
	calculate = user_open_order.calculate_total_price()
	total = calculate['total'].prefetch_related('product')
	context = {
		'order': total,
		'sum': calculate['total_amount'],
	}
	return render(request, 'user_panel_module/user_basket.html', context)


@login_required
def remove_order_detail(request):
	detail_id = request.GET.get('detail_id')
	if detail_id is None:
		return JsonResponse({'status': 'not_found_detail_id'})

	delete_count = OrderDetail.objects.filter(
		id=detail_id,
		order__is_paid=False,
		order__user_id=request.user.id
	).first()
	if delete_count is None:
		return JsonResponse({'status': 'detail_not_found'})
	else:
		delete_count.delete()
	user_open_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
	calculate = user_open_order.calculate_total_price()
	total = calculate['total'].prefetch_related('product')
	context = {
		'order': total,
		'sum': calculate['total_amount'],
	}
	return JsonResponse({
		'status': 'success',
		'body': render_to_string('user_panel_module/user_basket_content.html', context)
	})


@login_required
def change_order_detail_count(request):
	detail_id = request.GET.get('detail_id')
	state = request.GET.get('state')
	if detail_id is None or state is None:
		return JsonResponse({'status': 'not_found_detail_or_state'})

	order_detail = OrderDetail.objects.filter(
		id=detail_id, order__user_id=request.user.id,
		order__is_paid=False
	).first()
	if order_detail is None:
		return JsonResponse({'status': 'detail_not_found'})
	if state == 'increase':
		order_detail.count += 1
		order_detail.save()
	elif state == 'decrease':
		if order_detail.count == 1:
			order_detail.delete()
		else:
			order_detail.count -= 1
			order_detail.save()
	else:
		return JsonResponse({'status': 'state_invalid'})

	user_open_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
	calculate = user_open_order.calculate_total_price()
	total = calculate['total'].prefetch_related('product')
	context = {
		'order': total,
		'sum': calculate['total_amount'],
	}
	return JsonResponse({
		'status': 'success',
		'body': render_to_string('user_panel_module/user_basket_content.html', context)
	})


@login_required
def my_shopping_detail(request, order_id):
	order = Order.objects.filter(
		id=order_id,
		user_id=request.user.id,
		is_paid=True
	).prefetch_related('orderdetail_set').first()
	if order is None:
		raise Http404('سبد خرید مورد نظر یافت نشد')
	count_order_detail = {'count__sum': 0}
	# order = order.orderdetail_set.annotate(game_price=F('final_price') * F('count'))
	if order.orderdetail_set.count() != 1:
		count_order_detail = order.orderdetail_set.aggregate(Sum('count'))
	context = {
		'order': order,
		'count_orderdetail': count_order_detail.get('count__sum'),
	}
	return render(request, 'user_panel_module/user_shopping_detail.html', context)
