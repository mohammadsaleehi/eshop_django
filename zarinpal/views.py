from datetime import datetime

from django.conf import settings
import requests
import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from order_module.models import Order

# ? sandbox merchant
if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'

ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"

amount = 1000  # Rial / Required
description = "نهایی کردن خرید شما از سایت فروشگاه"  # Required
phone = ''  # Optional
# Important: need to edit for realy server.
CallbackURL = 'http://127.0.0.1:8000/verify-payment/'


@login_required
def send_request_payment(request):
    current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
    total_price = current_order.calculate_total_price()['total_amount']
    if total_price == 0:
        return redirect('user_basket_page')

    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": total_price * 10,
        "Description": description,
        # "Phone": phone,
        "CallbackURL": CallbackURL,
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    try:
        response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)

        if response.status_code == 200:
            response = response.json()
            if response['Status'] == 100:
                return {'status': True, 'url': ZP_API_STARTPAY + str(response['Authority']),
                        'authority': response['Authority']}
            else:
                return {'status': False, 'code': str(response['Status'])}
        return response

    except requests.exceptions.Timeout:
        return {'status': False, 'code': 'timeout'}
    except requests.exceptions.ConnectionError:
        return {'status': False, 'code': 'connection error'}


@login_required
def verify_payment(authority, request):
    current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
    total_price = current_order.caldculate_total_price()['total_amount']
    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": total_price * 10,
        "Authority": authority,
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    response = requests.post(ZP_API_VERIFY, data=data, headers=headers)

    if response.status_code == 200:
        response = response.json()
        if response['Status'] == 100:
            # return {'status': True, 'RefID': response['RefID']}
            current_order.is_paid = True
            current_order.payment_date = datetime.now()
            order_detail = current_order.orderdetail_set.all()
            for detail in order_detail:
                detail.final_price = detail.product.price
                detail.order.fianl_all_price = total_price
                detail.order.order_position = Order.OrderPosition.order_true
                detail.save()
            current_order.save()
            return render(request, 'zarinpal/psyment_result.html', {
                'success': f'تراکنش شما با کد پیگیری {response["RefID"]} با موفقیت انجام شد'
            })
        elif response['Status'] == 101:
            return render(request, 'zarinpal/psyment_result.html', {
                'info': f'این تراکنش قبلا ثبت شده است'
            })
        else:
            # return {'status': False, 'code': str(response['Status'])}
            return render(request, 'zarinpal/psyment_result.html', {
                'error': str(response['Status'])
            })
    return render(request, 'zarinpal/psyment_result.html', {
        'error': 'پرداخت با خطا مواجه شد / کاربر از پرداخت ممانعت کرد'
    })
