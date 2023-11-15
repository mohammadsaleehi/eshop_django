from django.urls import path

from . import views
app_name = "admin_app"
urlpatterns = [
    path('', views.index, name='admin_index'),
    path('articles/', views.ArticlesListView.as_view(), name='admin_articles'),
    path('article/add/', views.AddArticleView.as_view(), name='admin_add_article_page'),
    path('article/edit/<int:pk>/', views.ArticleEditView.as_view(), name='admin_edit_article'),
    path('article/delete/<int:pk>/', views.article_delete, name='admin_delete_article'),
]