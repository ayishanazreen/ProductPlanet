"""
URL configuration for ecom project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views
from django.contrib.auth import views as auth_view
from .forms import loginForm, MyPasswordResetForm, MyPasswordChangeForm, MySetPasswordForm

urlpatterns = [
    path("",views.home),
    path("category/<slug:val>", views.CategoryView.as_view(), name="categoryView"),
    path("Product_Details/<int:pk>", views.Product_Details.as_view(), name="Product_Details"),
    path("Category_title/<val>", views.CategoryTitle.as_view(), name="category_title"),
    path("about/", views.about,name="about"),
    path("contact/",views.contact,name="contact"),
    path("userCreation/",views.userRegistration.as_view(), name="userCreation"),
    path("profile/",views.ProfileView.as_view(),name="profile"),
    path("address/",views.address,name="address"),
    path("update_address/<int:pk>",views.update_address.as_view(),name="update_address"),
    path("paymentdone/", views.payment_done, name="paymentdone"),
    path("orders/", views.orders, name="orders"),
    path("plusWishlist/", views.plusWishlist),
    path("minusWishlist/", views.minusWishlist),
    path("search/", views.search, name="search"),
    path("wishlist/", views.wishlist, name="wishlist"),
 #Authentication 
    path("accounts/login/",auth_view.LoginView.as_view(template_name="login.html", authentication_form=loginForm), name="login"),
    path("password-change/", auth_view.PasswordChangeView.as_view(template_name="passwordChange.html", form_class=MyPasswordChangeForm, success_url='/passwordchangedone'),name="passwordChange"),
    path("passwordchangedone/", auth_view.PasswordChangeDoneView.as_view(template_name="passwordChangedone.html"),name="passwordChangedone"),
    path("logout/", auth_view.LogoutView.as_view(next_page="login"), name="logout"),
    path("add_cart/",views.add_cart, name="add_cart"),
    path("show_cart/",views.show_cart, name="show_cart"),
    path("plus_cart/",views.plus_cart),
    path("minus_cart/",views.minus_cart),
    path("remove_cart/",views.remove_cart),
    path("checkout/",views.checkout.as_view(), name="checkout"),


    #password reset

    path("password-reset/",auth_view.PasswordResetView.as_view(template_name="passwordReset.html", form_class=MyPasswordResetForm), name="PasswordReset"),

    path("password-reset/done",auth_view.PasswordResetDoneView.as_view(template_name="passwordResetDone.html"), name="password_reset_done"),

    path("password-reset-confirm/<uidb64>/<token>/",auth_view.PasswordResetConfirmView.as_view(template_name="passwordResetConfirm.html", form_class=MySetPasswordForm), name="password_reset_confirm"),

    path("password-reset-complete/",auth_view.PasswordResetCompleteView.as_view(template_name="passwordResetComplete.html"), name="password_reset_complete"),
]
