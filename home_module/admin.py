from django.contrib import admin
from .models import IPAddress


# Register your models here.

@admin.register(IPAddress)
class ArticleVisitAdmin(admin.ModelAdmin):
	list_display = ['ip_address', 'count_visit_product', "count_visit_article", 'id']

	@admin.display(description='تعداد مشاهده مقالات')
	def count_visit_article(self, obj):
		return obj.article_hits.count()

	@admin.display(description='تعداد مشاهده محصولات')
	def count_visit_product(self, obj):
		return obj.product_hits.count()
