from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404

from order_module.models import Order, OrderDetail
from product_module.models import Product


def add_product_to_order(request):
    product_id = request.GET.get('product_id')
    count = int(request.GET.get('count'))
    if count < 1:
        return JsonResponse({
            'status': 'invalid_count',
            'text': 'مقدار وارد شده معتبر نمی باشد',
            'confirm_button_text': 'مرسی از شما',
            'icon': 'warning'
        })

    if request.user.is_authenticated:
        product = Product.objects.filter(id=product_id, is_active=True, is_delete=False).first()
        if product:
            current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
            current_order_detail = current_order.orderdetail_set.filter(product_id=product_id).first()
            if current_order_detail:
                current_order_detail.count += count
                current_order_detail.save()
            else:
                now_detail = OrderDetail(order_id=current_order.id, product_id=product_id, count=count)
                now_detail.save()
            return JsonResponse({
                'status': 'success',
                'text': 'محصول مورد نظر شما با موفقیت به سبد خرید شما اضافه شد',
                'confirm_button_text': 'باشه ممنونم',
                'icon': 'success'
            })
        else:
            return JsonResponse({
                'status': 'not_found',
                'text': 'محصول مورد نظر یافت نشد',
                'confirm_button_text': 'مرسی',
                'icon': 'error'
            })
    else:
        # messages.error(request, 'برای افزودن محصول به سبد خرید ابتدا می بایست %s سایت شوید' % '<a href="/login/"><b>وارد</b></a>', extra_tags='danger')
        return JsonResponse({
            'status': 'not_auth',
            'text': 'برای افزودن محصول به سبد خرید ابتدا می بایست وارد سایت شوید',
            'confirm_button_text': '<a id="a_css" href="/login">ورود به سایت</a>',
            'icon': 'error'
        })
