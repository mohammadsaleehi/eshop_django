from django.urls import path

from . import views
app_name = "account"
urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register_page'),
    path('login/', views.LoginView.as_view(), name='login_page'),
    path('logout/', views.LogoutView.as_view(), name='logout_page'),
    path('forget-pass/', views.ForgotPasswordView.as_view(), name='forgot_password_page'),
    path('reset-pass/<active_code>/', views.ResetPassView.as_view(), name='reset_password_page'),
    path('activate-account/<str:email_active_code>/', views.ActivateAccountView.as_view(), name='activate_account')
]
