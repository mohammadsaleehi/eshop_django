from django.contrib import admin
from django.utils.html import format_html
from jalali_date import datetime2jalali
from jalali_date.admin import ModelAdminJalaliMixin

from account_module.models import User
from .models import ArticleCategory, Article, ArticleComment, ArticleHit

admin.site.site_header = 'مدیریت فروشگاه'
admin.site.site_title = 'مدیریت فروشگاه'
admin.site.index_title = 'مدیریت فروشگاه اینترنتی'


# admin.site.final_catch_all_view =

# admin.site.index_template = '404.html'
# admin.site.enable_nav_sidebar = False

class ArticleCategoryAdmin(admin.ModelAdmin):
	list_display = ['title', 'url_title', 'parent', 'is_active']
	list_editable = ['url_title', 'is_active', 'parent']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		if db_field.name == 'author':
			kwargs['queryset'] = User.objects.filter(is_superuser=True)
		return super().formfield_for_foreignkey(db_field, request, **kwargs)

	def formfield_for_manytomany(self, db_field, request, **kwargs):
		if db_field.name == 'selected_category':
			kwargs['queryset'] = ArticleCategory.objects.filter(parent__isnull=False)
		return super().formfield_for_manytomany(db_field, request, **kwargs)

	list_display = ['title', 'image_url', 'slug', 'category_article', 'is_active', 'author', 'article_visit_count']
	list_editable = ['is_active']
	list_filter = ['is_active']
	search_fields = ['title']
	search_help_text = 'این سرچ فقط برای عنوان عمل می کند'
	readonly_fields = ['created']
	prepopulated_fields = {'slug': ("title",)}
	fieldsets = [
		[None, {'fields': [('title', 'slug'), 'author', "is_active"]}],
		['فیلد های مربوط به نمایش', {"fields": ['image', "created", 'selected_category']}],
		['فیلد های نوشتاری', {"classes": ["collapse"], "fields": ['short_description', 'text']}],
		# ['تعداد بازدید', {'fields': ['hits_article']}],
	]
	filter_horizontal = ['selected_category']
	list_display_links = ['title', 'image_url']
	view_on_site = True

	@admin.display(description='تعداد بازدید')
	def article_visit_count(self, obj):
		return obj.hits_article.count()

	@admin.display(description='دسته بندی ها')
	def category_article(self, obj):
		return '، '.join([category.title for category in obj.selected_category.is_active_query()])

	@admin.display(description='تصویر مقاله')
	def image_url(self, obj):
		return format_html(f"<img width=172.4 height=79.6 style='border-radius: 10px' src='{obj.image.url}'>")


@admin.register(ArticleHit)
class ArticleHitAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
	list_display = ['ip_address', 'article', 'jalali_created']

	# you can override formfield, for example:

	# fields = ['ip_address', 'article', 'created']
	# readonly_fields = ('created',)
	@admin.display(description='زمان بازدید', ordering='created')
	def jalali_created(self, obj):
		return datetime2jalali(obj.created).strftime('%B %d %Y , ساعت %H:%M:%S')


class ArticleCommentAdmin(admin.ModelAdmin):
	list_display = ['user', 'parent', 'is_active']


# Register your models here.
admin.site.register(ArticleCategory, ArticleCategoryAdmin)
admin.site.register(ArticleComment, ArticleCommentAdmin)
