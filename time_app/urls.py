from django.urls import path     
from . import views
urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('shoppinglist', views.success),
    path('logout', views.logout),
    path('submit_product', views.submit_product),
    path('add_product', views.add_product),
    path('user/<user_id>', views.view_user_page),
    path('myaccount/<user_id>', views.see_account),
    path('edit_profile/<user_id>', views.edit_profile),
    path('destroy/<product_id>', views.delete_product),
    path('remove/<product_id>/<int:user_id>', views.remove_product)
]