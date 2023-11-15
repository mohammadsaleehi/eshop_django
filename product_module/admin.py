from django.contrib import admin
from django.utils.html import format_html
from jalali_date import datetime2jalali
from jalali_date.admin import ModelAdminJalaliMixin

from . import models


# Register your models here.
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
	# prepopulated_fields = {
	#     'slug': ['title']
	# }
	list_display = ['title', 'image_url', 'category_product', 'price', 'product_visit', 'is_active', 'is_delete']
	list_filter = ['is_active', 'category']
	list_editable = ['price', 'is_active', 'is_delete']

	# list_per_page = 4
	# list_max_show_all = 2
	# list_editable = ('title', 'price')
	# list_display_links = ('id',)
	# readonly_fields = ['slug']
	@admin.display(description='دسته بندی ها')
	def category_product(self, obj):
		return '، '.join([category.title for category in obj.category.all()])

	@admin.display(description='تعداد بازدید')
	def product_visit(self, obj):
		return obj.hits_product.count()

	@admin.display(description='تصویر محصول')
	def image_url(self, obj):
		if obj.image:
			return format_html(f"<img width=60 height=60 src='{obj.image.url}'>")
		return format_html(f"<img width=60 height=60 src='/static/images/product-details/1.jpg'>")


@admin.register(models.ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
	list_display = ['title', 'url_title', 'parent_valid_display', 'is_active', 'is_delete']
	list_filter = ['parent']
	list_editable = ['is_active', 'is_delete']
	search_fields = ['title', 'url_title']

	# prepopulated_fields = {'url_title': ['title']}
	@admin.display(description='دسته بندی والد (و) یا فرزند (ف)', ordering='parent')
	def parent_valid_display(self, obj: models.ProductCategory):
		if obj.parent:
			return "و: " + obj.parent.title
		else:
			return 'ف: ' + '، '.join([category.title for category in obj.product_category_parent.all()])


@admin.register(models.ProductTag)
class ProductTagAdmin(admin.ModelAdmin):
	pass


@admin.register(models.ProductBrand)
class ProductBrandAdmin(admin.ModelAdmin):
	list_display = ['title', 'url_title', 'is_active']
	list_editable = ['is_active']


@admin.register(models.ProductHit)
class ProductHitAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
	list_display = ['ip_address', 'product', 'jalali_created']

	@admin.display(description='زمان بازدید', ordering='created')
	def jalali_created(self, obj):
		return datetime2jalali(obj.created).strftime('%B %d %Y , ساعت %H:%M:%S')


# admin.site.register(models.ProductVisit)
admin.site.register(models.ProductGallery)
admin.site.register(models.ProductComment)
