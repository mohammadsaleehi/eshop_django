from ckeditor.fields import RichTextField
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse
from star_ratings.models import Rating

from account_module.models import User
from home_module.models import IPAddress
from datetime import datetime


class PollManager(models.Manager):
	def is_active_query(self):
		return self.filter(is_active=True)


class ArticleCategory(models.Model):
	parent = models.ForeignKey('ArticleCategory', null=True, blank=True, on_delete=models.CASCADE,
							   verbose_name='دسته بندی والد', related_name='category_valed')

	title = models.CharField(max_length=200, verbose_name='عنوان دسته بندی')
	url_title = models.CharField(max_length=200, unique=True, verbose_name='عنوان در url')
	is_active = models.BooleanField(default=True, verbose_name='فعال / غیر فعال')
	objects = PollManager()

	def __str__(self):
		return self.title

	class Meta:
		verbose_name = 'دسته بندی مقاله'
		verbose_name_plural = "دسته بندی های مقاله"


class Article(models.Model):
	title = models.CharField(max_length=300, verbose_name='عنوان مقاله')
	slug = models.SlugField(max_length=400, db_index=True, verbose_name='عنوان در url')
	image = models.ImageField(upload_to='images/articles/%Y/%m/%d/', verbose_name='تصویر مقاله')
	author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='نویسنده', null=True, blank=True)
	short_description = RichTextField(verbose_name='توضیحات کوتاه')
	text = RichTextField(verbose_name='متن مقاله')
	created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')
	is_active = models.BooleanField(default=True, verbose_name='فعال / غیر فعال')

	selected_category = models.ManyToManyField(ArticleCategory, verbose_name='دسته بندی ها')
	hits_article = models.ManyToManyField(IPAddress, through='ArticleHit', related_name='article_hits', blank=True,
										  verbose_name='مشاهده کننده ها')
	ratings = GenericRelation(Rating, related_query_name='foos', related_name='ratings_re')
	objects = PollManager()

	def get_absolute_url(self):
		return reverse('article:articles_detail', args=[self.pk, self.slug])

	def __str__(self):
		return self.title

	class Meta:
		verbose_name = 'مقاله'
		verbose_name_plural = "مقالات"


class ArticleComment(models.Model):
	article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='مقاله', related_name='comment_article')
	parent = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name='والد', null=True, blank=True,
							   related_name='parent_comment')
	user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
	created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')
	text = RichTextField(verbose_name='متن نظر')
	is_active = models.BooleanField(default=True, verbose_name='فعال / غیر فعال')
	objects = PollManager()

	class Meta:
		verbose_name = 'نظر مقاله'
		verbose_name_plural = 'نظرات مقاله'

	def __str__(self):
		return f'{self.id}/{self.user}/{self.article}'


class ArticleHit(models.Model):
	article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='مقاله')
	ip_address = models.ForeignKey(IPAddress, on_delete=models.CASCADE, verbose_name='کاربر')
	created = models.DateTimeField(default=datetime.now(), verbose_name='تاریخ بازدید')

	def __str__(self):
		return f'{self.article} / {self.ip_address} / {self.created}'

	class Meta:
		verbose_name = 'بازدید مقاله'
		verbose_name_plural = 'بازدیدهای مقالات'
