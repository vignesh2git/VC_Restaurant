from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.menu_list, name='menu_list'),
    path('dish/<int:pk>/', views.dish_detail, name='dish_detail'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:pk>/', views.cart_add, name='cart_add'),
    path('cart/dec/<int:pk>/', views.cart_decrement, name='cart_decrement'),
    path('cart/remove/<int:pk>/', views.cart_remove, name='cart_remove'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.order_history, name='order_history'),
    path('orders/<int:pk>/', views.order_summary, name='order_summary'),
    path('orders/<int:pk>/pay/', views.pay_order, name='pay_order'),
    path('orders/clear/', views.clear_order_history, name='orders_clear'),
    path('wishlist/toggle/<int:pk>/', views.wishlist_toggle, name='wishlist_toggle'),
    path('wishlist/', views.wishlist_page, name='wishlist_page'),
    path('promo/apply-coupon/', views.apply_coupon, name='apply_coupon'),
    path('promo/find/', views.find_promotion, name='find_promotion'),
    path('location/set-pincode/', views.set_pincode, name='set_pincode'),
    path('accounts/signup/', views.signup, name='signup'),

    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
]


