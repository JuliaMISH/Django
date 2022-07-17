from django.urls import path
# Импортируем созданное нами представление
from .views import home_view, contact_view, about_view, product_detail_view, product_create_view, dynamic_lookup_view, product_delete_view, product_list_view

app_name = 'testytest'

urlpatterns = [
    path('home/', home_view, name = 'home'),
    path('contact/', contact_view, name = 'contact'),
    path('about/', about_view, name = 'about'),
    path('detail/<int:id>/', product_detail_view, name = 'detail'),
    path('create/', product_create_view, name = 'create'),
    path('dyn/<int:id>/', dynamic_lookup_view, name='dynamic'),
    path('dyn/<int:id>/del/', product_delete_view, name = 'delete'),
    path('list/', product_list_view, name = 'list'),
]