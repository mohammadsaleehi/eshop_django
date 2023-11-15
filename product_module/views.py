from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.postgres.search import TrigramSimilarity
from django.db import connection
from django.db.models import Count, Sum, Q
from django.db.models.functions import Greatest
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from site_module.models import SiteBanner
from utils.convertors import group_list
from .models import Product, ProductCategory, ProductBrand, ProductGallery, ProductComment


class ProductListView(ListView):
	template_name = 'product_module/post/product_list.html'
	model = Product
	context_object_name = 'products'
	paginate_by = 9
	queryset = model.objects.is_active_query()

	def get_queryset(self, *args, **kwargs):
		data = super(ProductListView, self).get_queryset()
		category = self.kwargs.get('category')
		brand = self.kwargs.get('brand')
		search = self.request.GET.get('search')

		start_price = self.request.GET.get('start_price')
		end_price = self.request.GET.get('end_price')
		if search:
			data = data.annotate(
				similarity=Greatest(TrigramSimilarity('title', search), TrigramSimilarity('short_description', search),
									TrigramSimilarity('description', search))).filter(similarity__gt=0.05).order_by(
				'-similarity')
		if category:
			data = data.filter(category__url_title__iexact=category)
		if brand:
			data = data.filter(brand__url_title__iexact=brand).order_by('-id').distinct()
		if start_price:
			data = data.filter(price__gte=start_price)
		if end_price:
			data = data.filter(price__lte=end_price)
		ord = self.request.GET.get('ord')
		if ord == 'old':
			data = data.order_by('id')
		elif ord == 'visit':
			data = data.annotate(visit_count=Count('hits_product')).order_by('-visit_count')
		elif ord == 'visit-30':
			last_month = datetime.today() - timedelta(days=30)
			data = data.annotate(count=Count('hits_product', filter=Q(producthit__created__gt=last_month))).order_by(
				'-count')
		elif ord == 'seller':
			data = data.annotate(
				order_count=Sum('orderdetail__count', filter=Q(orderdetail__order__is_paid=True))).order_by(
				'-order_count')
		elif ord == 'expensive':
			data = data.order_by('-price', '-id')
		elif ord == 'cheap':
			data = data.order_by('price', '-id')
		return data

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super(ProductListView, self).get_context_data()
		query = self.queryset
		product = query.order_by('-price').first()
		db_max_price = product.price if product else 1000000
		search = self.request.GET.get('search')
		if search:
			context['search'] = search or None

		context['db_max_price'] = db_max_price
		context['start_price'] = self.request.GET.get('start_price') or 0
		context['end_price'] = self.request.GET.get('end_price') or db_max_price
		context['banners'] = SiteBanner.objects.filter(is_active=True,
													   position__iexact=SiteBanner.SiteBannerPosition.product_list)
		return context


class ProductDetailView(DetailView):
	template_name = 'product_module/post/product_detail.html'
	model = Product

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		loaded_product = self.object
		request = self.request
		context['banners'] = SiteBanner.objects.filter(is_active=True,
													   position__iexact=SiteBanner.SiteBannerPosition.product_detail)
		galleries = list(ProductGallery.objects.filter(product_id=loaded_product.id))
		galleries.insert(0, loaded_product)
		context['product_galleries_group'] = group_list(galleries, 3)
		context['related_product'] = group_list(list(
			Product.objects.is_active_query().filter(brand_id=loaded_product.brand_id).exclude(id=loaded_product.id)[
			:9]), 3)
		context['comments'] = ProductComment.objects.is_active_q().filter(product_id=loaded_product.id).order_by(
			'-created')
		user_ip = request.user.ip_address
		if user_ip not in loaded_product.hits_product.all():
			loaded_product.hits_product.add(user_ip)
		return context


def product_category_component(request):
	categorys = ProductCategory.objects.filter(is_active=True, parent_id=None).prefetch_related(
		'product_category_parent')
	context = {
		'category': categorys
	}
	return render(request, 'product_module/component/product_category_component.html', context)


def brand_component(request):
	brand = ProductBrand.objects.filter(is_active=True, brand_product__is_active=True,
										brand_product__is_delete=False).annotate(
		products_count=Count('brand_product')).order_by(
		'-products_count')
	context = {
		'brands': brand,
	}
	return render(request, 'product_module/component/category_brand_page.html', context)


def send_comment_product(request):
	if request.user.is_authenticated:
		product_id = request.GET.get('product_id')
		product_comment = request.GET.get('product_comment')
		now_comment = ProductComment(product_id=product_id, text=product_comment, user_id=request.user.id)
		now_comment.save()
		messages.success(request, 'کامنت شما ارسال شد', 'success')
		comments = ProductComment.objects.is_active_q().filter(product_id=product_id).order_by('-created')
		context = {
			'comments': comments,
			'product_id': product_id
		}
		return render(request, 'product_module/includes/product_comment_partial.html', context)
	return HttpResponse('No send comment you!')
