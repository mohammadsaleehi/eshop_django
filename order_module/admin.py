from django.contrib import admin
from jalali_date import datetime2jalali

from order_module.models import Order, OrderDetail

# admin.site.site_header = 'مدیریت سایت'


@admin.action(description="نهایی شود")
def make_is_paid(modeladmin, request, queryset):
    rows_update = queryset.update(is_paid=True)
    modeladmin.message_user(request, '%s سبد خرید به نهایی شود تغییر کردند' % rows_update)


@admin.action(description="نهایی نشود")
def make_is_unpaid(modeladmin, request, queryset):
    rows_update = queryset.update(is_paid=False)
    modeladmin.message_user(request, '%s سبد خرید به نهایی نشود تغییر کردند' % rows_update)


@admin.action(description="وضعیت به در حال سفارش تغییر کند")
def make_position_product(modeladmin, request, queryset):
    rows_update = queryset.update(order_position=Order.OrderPosition.order_product)
    modeladmin.message_user(request, 'وضعیت %s سبد خرید به در حال سفارش تغییر کردند' % rows_update)


@admin.action(description="وضعیت به در حال بررسی تغییر کند")
def make_position_visit(modeladmin: Order, request, queryset):
    rows_update = queryset.update(order_position=Order.OrderPosition.order_visit)
    if rows_update == 1:
        message_bit = "تغییر کرد"
    else:
        message_bit = "تغییر کردند"
    modeladmin.message_user(request, "وضعیت %s سبد خرید به در حال بررسی %s" % (rows_update, message_bit))


@admin.action(description="وضعیت به در حال ارسال تغییر کند")
def make_position_arial(modeladmin, request, queryset):
    rows_update = queryset.update(order_position=Order.OrderPosition.order_arial)
    modeladmin.message_user(request, 'وضعیت %s سبد خرید به در حال ارسال تغییر کردند' % rows_update)


@admin.action(description="وضعیت به در حال در حال دسته بندی تغییر کند")
def make_position_category(modeladmin, request, queryset):
    rows_update = queryset.update(order_position=Order.OrderPosition.order_category)
    modeladmin.message_user(request, 'وضعیت %s سبد خرید به در حال دسته بندی تغییر کردند' % rows_update)


@admin.action(description="وضعیت به در حال تکمیل شد تغییر کند")
def make_position_true(modeladmin, request, queryset):
    rows_update = queryset.update(order_position=Order.OrderPosition.order_true)
    modeladmin.message_user(request, 'وضعیت %s سبد خرید به در حال تکمیل شد تغییر کردند' % rows_update)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'payment_date_display', 'order_position', 'final_all_price_display', 'is_paid']
    list_filter = ['order_position', 'is_paid']
    list_editable = ['order_position']
    list_display_links = ['user']
    date_hierarchy = 'payment_date'
    search_fields = ['user__email', 'final_all_price']
    actions = [make_is_paid, make_is_unpaid, make_position_product, make_position_visit, make_position_category,
               make_position_arial, make_position_true]

    @admin.display(description='تاریخ پرداخت فاکتور', ordering='payment_date')
    def payment_date_display(self, obj):
        if obj.payment_date:
            return datetime2jalali(obj.payment_date).strftime('T: %Y-%b-%d, %H:%M:%S')
        return '_'

    @admin.display(description='پرداخت کل فاکتور', ordering='final_all_price')
    def final_all_price_display(self, obj):
        if obj.final_all_price:
            return '{:,}'.format(obj.final_all_price)
        else:
            return '-'


@admin.register(OrderDetail)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'order_id_display', 'product', 'final_price', 'count']
    list_editable = ['final_price', 'count']
    list_filter = ['order_id', 'order__is_paid']
    list_display_links = ['product']
    search_fields = ['order__id']

    @admin.display(description='آی دی سبد خرید', ordering='order_id')
    def order_id_display(self, obj):
        return obj.order.id
