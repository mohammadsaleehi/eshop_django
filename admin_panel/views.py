from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, UpdateView, CreateView

from account_module.models import User
# from .mixins import FieldsMixin, FormValidMixin
from admin_panel.forms import ArticleUpdateForm
from article_module.models import Article, ArticleCategory
from utils.my_decorators import permission_checker_decorator_factory


# Create your views here.
@permission_checker_decorator_factory()
def index(request):
	return render(request, 'admin_panel/home/index.html')


@method_decorator(permission_checker_decorator_factory(), name='dispatch')
class ArticlesListView(ListView):
	model = Article
	context_object_name = 'articles'
	paginate_by = 12
	template_name = 'admin_panel/articles/articles_list.html'

	def get_queryset(self, *args, **kwargs):
		data = super(ArticlesListView, self).get_queryset()
		if not self.request.user.is_superuser:
			data = data.filter(author=self.request.user)

		category_name = self.kwargs.get('category')
		if category_name is not None:
			data = data.filter(selected_category__url_title__iexact=category_name)
		order_article = self.request.GET.get('order_by')
		order_method_articles = (
			'id', '-id', 'title', '-title', 'slug', '-slug',
			'short_description', '-short_description', 'is_active', '-is_active'
		)
		if order_article in order_method_articles:
			data = data.order_by(order_article)
		else:
			data = data.order_by('-created')
		return data


@method_decorator(permission_checker_decorator_factory(), name='dispatch')
class ArticleEditView(UpdateView):
	model = Article
	template_name = 'admin_panel/articles/edit_article.html'
	form_class = ArticleUpdateForm
	# success_url = '/admin-panel/articles/'
	success_url = reverse_lazy('admin_app:admin_articles')

	def get_form_kwargs(self):
		kwargs = super(ArticleEditView, self).get_form_kwargs()
		kwargs.update({
			'user': self.request.user
		})
		return kwargs


@permission_checker_decorator_factory()
def article_delete(request, pk):
	article = get_object_or_404(Article, pk=pk)
	article.delete()
	return redirect('admin_app:admin_articles')


# class AddArticleView(FormValidMixin, FieldsMixin, CreateView):
@method_decorator(permission_checker_decorator_factory(), name='dispatch')
class AddArticleView(CreateView):
	model = Article
	fields = '__all__'
	# form_class = ArticleUpdateForm
	template_name = 'admin_panel/articles/add_article.html'
	success_url = reverse_lazy('admin_app:admin_articles')

	def get_form(self, form_class=None):
		form = super().get_form(form_class)
		form.fields['selected_category'].queryset = ArticleCategory.objects.filter(parent__isnull=False)
		form.fields['author'].queryset = User.objects.filter(is_superuser=True, is_active=True)
		return form
