from datetime import datetime

from django.db import models
from django.urls import reverse

from account_module.models import User
from home_module.models import IPAddress


class ActiveAndDeleteManager(models.Manager):
	def is_active_query(self):
		return self.filter(is_active=True, is_delete=False)


class ActiveManager(models.Manager):
	def is_active_q(self):
		return self.filter(is_active=True)


class ProductCategory(models.Model):
	title = models.CharField(max_length=300, db_index=True, verbose_name='عنوان')
	url_title = models.CharField(max_length=300, db_index=True, verbose_name='عنوان در url')
	parent = models.ForeignKey('ProductCategory', on_delete=models.CASCADE, null=True, verbose_name='دسته بندی والد',
							   related_name='product_category_parent', blank=True)
	is_active = models.BooleanField(default=False, verbose_name='فعال / غیرفعال')
	is_delete = models.BooleanField(verbose_name='حذف شده/ نشده')

	def __str__(self):
		return f'( {self.title} - {self.url_title})'

	class Meta:
		verbose_name = 'دسته بندی'
		verbose_name_plural = 'دسته بندی ها'


class ProductBrand(models.Model):
	title = models.CharField(max_length=300, verbose_name='نام برند', db_index=True)
	url_title = models.CharField(max_length=300, verbose_name='نام برند در url', db_index=True)
	is_active = models.BooleanField(verbose_name='فعال / غیر فعال')

	class Meta:
		verbose_name = 'برند'
		verbose_name_plural = 'برند ها'

	def __str__(self):
		return self.title


class Product(models.Model):
	title = models.CharField(max_length=135, name='title', verbose_name='کپشن')
	category = models.ManyToManyField(
		ProductCategory,
		related_name='product_categories',
		verbose_name='دسته بندی'
	)
	image = models.ImageField(upload_to='images/products/%Y/%m/%d/', null=True, blank=True, verbose_name='تصویر محصول')
	brand = models.ForeignKey(ProductBrand, on_delete=models.SET_NULL, verbose_name='برند', null=True, blank=True,
							  related_name='brand_product')
	price = models.IntegerField(verbose_name='قیمت')
	short_description = models.CharField(max_length=360, db_index=True, null=True, verbose_name='توضیحات کوتاه')
	description = models.TextField(verbose_name='توضیحات اصلی', db_index=True)
	slug = models.SlugField(default='', null=False, db_index=True, blank=True, max_length=200, unique=True)
	is_active = models.BooleanField(default=False, verbose_name='فعال / غیرفعال')
	is_delete = models.BooleanField(verbose_name='حذف شده/ نشده')
	hits_product = models.ManyToManyField(IPAddress, through='ProductHit', related_name='product_hits', blank=True,
										  verbose_name="بازدیدکننده ها")
	objects = ActiveAndDeleteManager()

	def get_absolute_url(self):
		return reverse('product-detail', args=[self.id, self.slug])

	def save(self, *args, **kwargs):
		# self.slug = slugify(self.title)
		super().save(*args, **kwargs)

	def __str__(self):
		return "%s (%s)" % (self.title, self.price)

	def get_image_url(self):
		if self.image:
			return self.image.url
		else:
			return None

	class Meta:
		verbose_name = 'محصول'
		verbose_name_plural = 'محصولات'
		ordering = ['-id']


class ProductTag(models.Model):
	caption = models.CharField(max_length=300, db_index=True, verbose_name='عنوان')
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_tags')

	def __str__(self):
		return self.caption

	class Meta:
		verbose_name = 'تگ محصول'
		verbose_name_plural = "تگ های محصولات"


# class ProductVisit(models.Model):
# 	product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول', related_name='product_visit')
# 	ip = models.CharField(max_length=30, verbose_name='آی پی کاربر')
# 	user = models.ForeignKey(User, null=True, blank=True, verbose_name='کاربری که مشاهده کرده',
# 							 on_delete=models.CASCADE)
#
# 	def __str__(self):
# 		return f'{self.product.title} / {self.ip}'
#
# 	class Meta:
# 		verbose_name = 'بازدید ها محصول'
# 		verbose_name_plural = "بازدید های محصول"


class ProductGallery(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
	image = models.ImageField(upload_to='images/products-gallery/%Y/%m/%d', verbose_name='تصویر')

	def __str__(self):
		return self.product.title

	class Meta:
		verbose_name = 'تصویر گالری'
		verbose_name_plural = "گالری تصاویر"


class ProductComment(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
	user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
	created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')
	text = models.TextField(verbose_name='متن نظر')
	is_active = models.BooleanField(default=True, verbose_name='فعال / غیر فعال')

	objects = ActiveManager()

	class Meta:
		verbose_name = 'نظر محصول'
		verbose_name_plural = 'نظرات محصولات'

	def __str__(self):
		return f'{self.user}'


class ProductHit(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول مشاهده شده')
	ip_address = models.ForeignKey(IPAddress, on_delete=models.CASCADE, verbose_name='کاربر که مشاهده کرده')
	created = models.DateTimeField(default=datetime.today(), verbose_name='زمان مشاهده')

	def __str__(self):
		return f'{self.ip_address} / {self.product} / {self.created}'

	class Meta:
		verbose_name = 'بازدید محصول'
		verbose_name_plural = 'بازدید محصولات'
