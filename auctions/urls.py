from django.urls import path

from . import views

app_name = 'auctions'

urlpatterns = [
    path("", views.index, name="index"),
    path('publisher/about', views.about, name='about_publisher'),
    path('product/create', views.ProductCreate.as_view(), name='product_create'),
    path("search/<slug:category_slug>/", views.category_list, name="category_list"),
    path("item/<slug:slug>/", views.product_detail, name="product_detail"),
    path("item/<slug:slug>/bid/", views.make_bid, name="make_bid"),
    path("item/<slug:slug>/comment/", views.give_comment, name="give_comment"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
]
