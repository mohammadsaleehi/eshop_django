from django.urls import path
from . import views


urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
    path('cat/category/<str:category>/', views.ProductListView.as_view(), name='cat-product-list-category'),
    path('cat/brand/<str:brand>/', views.ProductListView.as_view(), name='cat-product-list-brand'),
    path('detail/<int:pk>/<slug:slug>/', views.ProductDetailView.as_view(), name="product-detail"),
    path('add-product-comment/', views.send_comment_product, name='send_comment_product')
]