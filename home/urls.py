from home import views
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.main, name='main'),
    path('faq/', views.faq, name='faq'),
    path('order/', views.order, name='order'),
    path('search/', views.search, name='search'),
    path('client/', views.client, name='client'),
    path('contact/', views.contact, name='contact'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('newshop/', views.newshop, name='newshop'),
    path('payment/', views.payment, name='payment'),
    path('shopcart/', views.shopcart, name='shopcart'),
    path('search_product/', views.search_product, name='search_product'),
    path('loading_page/', views.loading_page, name='loading_page'),
########################################################################################################################
    path('delete_cart/<int:id>/', views.delete_cart, name='delete_cart'),
    path('news_detail/<str:code>/', views.news_detail, name='news_detail'),
    path('order_detail/<str:code>/', views.order_detail, name='order_detail'),
    path('product_detail/<str:code>/', views.product_detail, name='product_detail'),
    path('filter_products/<str:code>/', views.filter_products, name='filter_products'),
########################################################################################################################
    path('ShopCart/', views.ShopCart.as_view(), name='ShopCart'),
    path('ContactUs/', views.ContactUs.as_view(), name='ContactUs'),
    path('PaymentPrice/<int:id>/', views.PaymentPrice.as_view(), name='PaymentPrice'),
    path('OrderProduct/', views.OrderProduct.as_view(), name='OrderProduct'),
    path('Comment_to_News/', views.Comment_to_News.as_view(), name='Comment_to_News'),
    path('Comment_to_Product/', views.Comment_to_Product.as_view(), name='Comment_to_Product'),
    path('UpdateTotalPriceAPIView/', views.UpdateTotalPriceAPIView.as_view(), name='UpdateTotalPriceAPIView'),
########################################################################################################################
    path('register/', views.register.as_view(), name='register'),
    path('login_form/', views.login_form, name='login_form'),
    path('verify_code/', views.verify_code, name='verify_code'),
    path('update/', views.update, name='update'),
    path('password/', views.password, name='password'),
    path('logout_client/', views.logout_client, name='logout_client'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='Authenticate/password_reset_form.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='Authenticate/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<slug:uidb64>/<slug:token>/', auth_views.PasswordResetConfirmView.as_view(template_name='Authenticate/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='Authenticate/password_reset_complete.html'), name='password_reset_complete'),
########################################################################################################################
]