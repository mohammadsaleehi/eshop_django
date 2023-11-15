from django.db import models
from django.db.models import F, Sum

from account_module.models import User
from product_module.models import Product


class Order(models.Model):
    class OrderPosition(models.TextChoices):
        order_product = 'order_product', 'در حال سفارش',
        order_visit = 'order_visit', 'در حال بررسی',
        order_category = 'order_category', 'در حال دسته بندی',
        order_arial = 'order_arial', 'در حال ارسال',
        order_true = 'order_true', 'سفارش تکمیل شد',

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    is_paid = models.BooleanField(verbose_name='نهایی شده / نشده')
    payment_date = models.DateTimeField(null=True, blank=True, verbose_name='تاریخ پرداخت')
    order_position = models.CharField(max_length=300, choices=OrderPosition.choices, verbose_name='وضعیت سفارش',
                                      default=OrderPosition.order_product)
    final_all_price = models.IntegerField(verbose_name='مقدار پرداخت کل', null=True, blank=True)

    def __str__(self):
        return f'{self.user} / {self.id}'

    def calculate_total_price(self):
        if self.is_paid:
            total = self.orderdetail_set.annotate(total_price=F('final_price') * F('count'))
            total_amount = total.aggregate(Sum('total_price'))['total_price__sum'] or 0
        else:
            total = self.orderdetail_set.annotate(total_price=F('product__price') * F('count'))
            total_amount = total.aggregate(Sum('total_price'))['total_price__sum'] or 0
        return {
            'total': total,
            'total_amount': total_amount,
        }

    def calculate_total_final_price(self):
        if self.is_paid:
            total = self.orderdetail_set.annotate(total_price=F('final_price') * F('count'))
            total_amount = total.aggregate(Sum('total_price'))['total_price__sum'] or 0
        else:
            total = self.orderdetail_set.annotate(total_price=F('product__price') * F('count'))
            total_amount = total.aggregate(Sum('total_price'))['total_price__sum'] or 0
        return total_amount

    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = "سبد های خرید کاربران"


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='سبد خرید')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    final_price = models.IntegerField(null=True, blank=True, verbose_name='قیمت نهایی تکی محصول')
    count = models.IntegerField(verbose_name='تعداد')

    def __str__(self):
        return str(self.order)

    def total_price_count(self):
        return self.final_price * self.count

    class Meta:
        verbose_name = 'جزییات سبد خرید'
        verbose_name_plural = "لیست جزییات سبدهای خرید"
