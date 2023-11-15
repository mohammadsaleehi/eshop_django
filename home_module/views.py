
from django.db.models import Count, Sum
from django.shortcuts import render
from django.views.generic.base import TemplateView

from product_module.models import Product, ProductCategory
from site_module.models import SiteSetting, FooterLinkBox, Slider
from utils.convertors import group_list


class HomeView(TemplateView):
	template_name = 'home_module/index_page.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['sliders'] = Slider.objects.filter(is_active=True)
		latest_products = Product.objects.filter(is_active=True, is_delete=False).order_by('-id')[:12]
		most_visit_product = Product.objects.filter(is_active=True, is_delete=False).annotate(
			visit_count=Count('hits_product')).order_by('-visit_count')[:12]
		context['latest_products'] = group_list(latest_products, 4)
		context['most_visit_product'] = group_list(most_visit_product)
		categories = list(
			ProductCategory.objects.annotate(product_count=Count('product_categories')).filter(is_active=True,
																							   is_delete=False,
																							   product_count__gt=0)[:10]
		)
		categories_products = []
		for category in categories:
			item = {
				'title': category.title,
				'id': category.id,
				'products': list(category.product_categories.all()[:4])
			}
			categories_products.append(item)

		context['categories_products'] = categories_products
		most_bought_products = Product.objects.filter(orderdetail__order__is_paid=True).annotate(order_count=Sum(
			'orderdetail__count'
		)).order_by('-order_count')[:12]
		context['most_bought_products'] = group_list(most_bought_products)
		return context


def site_header_component(request):
	setting = SiteSetting.objects.filter(is_main_setting=True).only('site_logo').first()

	context = {
		'site_setting': setting
	}
	return render(request, 'shared/site_header_component.html', context)


def site_footer_component(request):
	setting = SiteSetting.objects.filter(is_main_setting=True).only('site_name', 'about_us_text', 'copy_right').first()
	footer_link_box = FooterLinkBox.objects.all().only('title', ).prefetch_related('footerlink_set')
	context = {
		'site_setting': setting,
		'footer_link_boxs': footer_link_box
	}
	return render(request, 'shared/site_footer_component.html', context)


class AboutView(TemplateView):
	template_name = 'home_module/about.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		setting = SiteSetting.objects.filter(is_main_setting=True).defer('site_url', 'copy_right').first()
		context['site_setting'] = setting
		return context
