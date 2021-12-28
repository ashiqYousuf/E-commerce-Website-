from django.urls import path
from accounts import views
from django.contrib.auth import views as auth_views
from .forms import CustomPasswordResetForm , CustomSetPasswordForm



urlpatterns = [
    path('',views.all_products,name='all_products'),
    # Below 2 urls are same for django so use slash with one & not with one
    path('<int:slug>/',views.product_detail,name='product_detail'),
    path('filter/<str:slug>',views.categories,name='categories'),
    path('signup/',views.user_signup,name='signup'),
    path('login/',views.user_login,name='login'),
    path('profile/',views.user_profile,name='profile'),
    path('logout/',views.user_logout,name='logout'),
    path('changepassword/',views.change_password,name='change_password'),

    # Password Management 
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html',form_class=CustomPasswordResetForm),name='password_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html',form_class=CustomSetPasswordForm), name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),name='password_reset_complete'),
    # End of password Management
    path('profile/add/',views.add_address,name='add_address'),
    path('search/',views.search_product,name='search_product'),

    path('add-to-cart/',views.add_to_cart,name='add-to-cart'),
    path('cart/',views.show_cart,name='show_cart'),
    path('remove-item/<int:id>/',views.remove_item,name='remove_item'),
    path('checkout/',views.checkout,name='checkout'),
    path('orders/',views.orders,name='orders'),
]
