from django import forms

from article_module.models import Article


class ArticleUpdateForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		user = kwargs.pop('user',)
		super(ArticleUpdateForm, self).__init__(*args, **kwargs)
		if not user.is_superuser:
			self.fields['author'].disabled = True

	class Meta:
		model = Article
		fields = "__all__"
