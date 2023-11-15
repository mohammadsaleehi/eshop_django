from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.urls import path

from user_panel_module import views

urlpatterns = [
    path('', views.user_panel_dashboard_page, name='user_panel_dashboard'),
    path('edit-profile/', views.EditUserProfilePage.as_view(), name='edit_profile_page'),
    path("change-password/", PasswordChangeView.as_view(), name='change_password_page'),
    path("change-password/done/", PasswordChangeDoneView.as_view(), name='password_change_done'),
    path("user-basket/", views.user_basket, name='user_basket_page'),
    path("my-shoppings/", views.MyShopping.as_view(), name='user_shoppings_page'),
    path("my-shopping-detail/<int:order_id>/", views.my_shopping_detail, name='user_shopping_detail_page'),
    path("remove-order-detail", views.remove_order_detail, name='remove_order_detail_ajax'),
    path('change-order-detail', views.change_order_detail_count, name='change_order_detail_ajax'),
]
