from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Count, Q
from django.db.models.functions import Greatest

from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView

from .models import Article, ArticleCategory, ArticleComment
from utils.my_decorators import permission_checker_decorator_factory


# Create your views here.

class ArticlesListView(ListView):
	model = Article
	context_object_name = 'articles'
	paginate_by = 3
	template_name = 'article_module/articles_page.html'
	queryset = model.objects.is_active_query().annotate(
		hit_article_view=Count('hits_article')
	).defer('text', 'is_active').order_by('-created')

	# queryset =
	def get_queryset(self, *args, **kwargs):
		base_query = super(ArticlesListView, self).get_queryset()
		category_name = self.kwargs.get('category')
		search = self.request.GET.get('search')
		if search is not None:
			base_query = base_query.annotate(
				similarity=Greatest(TrigramSimilarity('title', search),
									TrigramSimilarity('short_description', search),
									TrigramSimilarity('text', search))
			).filter(similarity__gt=0.05).order_by('-similarity')
		last_month = datetime.today() - timedelta(days=30)
		if category_name is not None:
			base_query = base_query.filter(selected_category__url_title__iexact=category_name)
		order_article = self.request.GET.get('order')
		if order_article == 'old':
			base_query = base_query.order_by('created')
		elif order_article == 'visited':
			base_query = base_query.annotate(count=Count('hits_article')).order_by('-count')
		elif order_article == 'visit_30':
			base_query = base_query.annotate(
				count=Count('hits_article', filter=Q(articlehit__created__gt=last_month))
			).order_by('-count', '-articlehit__created')
		elif order_article == 'hot':
			base_query = base_query.annotate(
				chg=Count('comment_article', filter=Q(comment_article__created__gt=last_month))
			).order_by('-chg')
		elif order_article == 'popular':
			base_query = base_query.filter(ratings__isnull=False).order_by('-ratings__average')
		return base_query

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		search = self.request.GET.get('search')
		if search:
			context['search'] = search

		return context


class ArticleDetailView(DetailView):
	model = Article
	template_name = 'article_module/article_detail_page.html'
	context_object_name = 'article'
	queryset = model.objects.is_active_query()

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		article = self.object
		comments = ArticleComment.objects.is_active_query().filter(article_id=article.id) \
			.prefetch_related('parent_comment').order_by('-created')
		context['comments'] = comments.filter(parent_id=None)
		context['comments_count'] = len(comments)
		ip_address = self.request.user.ip_address
		if ip_address not in iter(article.hits_article.all()):
			article.hits_article.add(ip_address)
		return context


@method_decorator(permission_checker_decorator_factory(), name='dispatch')
class ArticlePreview(DetailView):
	model = Article
	template_name = 'article_module/article_detail_page.html'
	context_object_name = 'article'

	def dispatch(self, request, *args, **kwargs):
		article = Article.objects.filter(pk=kwargs.get('pk'), slug=kwargs.get('slug')).first()
		if article.is_active:
			return redirect('article:articles_detail', pk=kwargs.get('pk'), slug=kwargs.get('slug'))
		messages.info(request, 'این مقاله در حالت پیش نمایش است فقط برای ادمین ها نمایش داده می شود')
		return super().dispatch(request, *args, **kwargs)


def article_category_components(request):
	article_main_categories = ArticleCategory.objects.is_active_query().filter(parent_id=None). \
		prefetch_related('category_valed')
	context = {
		'main_categories': article_main_categories
	}
	return render(request, 'article_module/components/article_category_components.html', context)


@login_required()
def add_article_comment(request):
	article_id = request.GET.get('article_id')
	article_comment = request.GET.get('article_comment')
	parent_id = request.GET.get('parent_id')
	now_comment = ArticleComment(
		article_id=article_id, text=article_comment,
		user_id=request.user.id, parent_id=parent_id
	)
	now_comment.save()
	comments = ArticleComment.objects.is_active_query().filter(article_id=article_id).\
		prefetch_related('parent_comment').order_by('-created')
	context = {
		'comments': comments.filter(parent_id__isnull=True),
		'comments_count': len(comments)
	}
	return render(request, 'inclouds/article_comment_partial.html', context)


def article_popular_component(request):
	last_month = datetime.today() - timedelta(days=30)
	popular_articles = Article.objects.is_active_query().annotate(
		count=Count('hits_article', filter=Q(articlehit__created__gt=last_month))
	).order_by('-count', '-articlehit__created').only('slug', 'title')[:5]
	context = {
		'popular_articles': popular_articles
	}
	return render(request, 'article_module/components/article_popular.html', context)
