from django.urls import path

from . import views
app_name = "article"
urlpatterns = [
    path('', views.ArticlesListView.as_view(), name='articles_list'),
    path('cat/<str:category>/', views.ArticlesListView.as_view(), name='articles_by_category_list'),
    path('detail/<int:pk>/<slug:slug>/', views.ArticleDetailView.as_view(), name='articles_detail'),
    path('add-article-comment/', views.add_article_comment, name='add_article_comment'),
    path('preview/<int:pk>/<slug:slug>/', views.ArticlePreview.as_view(), name="article_preview_admin")
]
