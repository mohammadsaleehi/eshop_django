from django import template
from jalali_date import datetime2jalali, date2jalali

register = template.Library()


@register.filter(name='jalali_date')
def jalali_date(date, formt=False):
	return date2jalali(date).strftime(formt)


@register.filter(name='jalali_time')
def jalali_time(data, formt=False):
	return datetime2jalali(data).strftime(formt)


@register.filter(name='price_como')
def price_c(data):
	return '{:,}'.format(data) + ' ت'


@register.simple_tag()
def login_url_product_detail(login, product_detail):
	return f'{login}?next={product_detail}'
