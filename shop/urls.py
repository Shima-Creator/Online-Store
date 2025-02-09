from itertools import product

from pygments.lexer import include

from shop import views
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static


url_lists = [
    path('categories_list/', views.CategoriesListView.as_view(), name='categories'),
    path('product_list/', views.ProductListView.as_view(), name='products'),
    path('salesman_list/', views.SalesmanListView.as_view(), name='salesmans'),
]

url_jsons = [
    path('api/categories_list/', views.CategoryAPIView.as_view(), name='json_cat_all'),
    path('api/categories_list/<int:pk>', views.CategoryAPIView.as_view(), name='json_cat'),
    path('api/product_list/', views.ProductAPIView.as_view(), name='json_products_all'),
    path('api/product_list/<int:pk>', views.ProductAPIView.as_view(), name='json_product'),
    path('api/salesman_list/', views.SalesmanAPIView.as_view(), name='json_salesmans_all'),
    path('api/salesman_list/<int:pk>', views.SalesmanAPIView.as_view(), name='json_salesman'),
    path('api/subcategories_list/',views.SubCategoryAPIView.as_view(), name='json_subcat_all'),
    path('api/subcategories_list/<int:pk>',views.SubCategoryAPIView.as_view(), name='json_subcat'),
    path('api/basket/', views.BasketAPIView.as_view(), name='json_basket_all'),
    path('api/basket/<int:pk>', views.BasketAPIView.as_view(), name='json_basket'),
]

url_orders = [
    # path('create_order/', views.CreateOrderView.as_view(), name='create_order'),
    # path('order_success/', views.OrderSuccessView.as_view(), name='order_success'),
]

url_products = [
    path('search/', views.search_product, name='search_product'),
    path('update-quantity/', views.add_quantity_basket_product, name='update_quantity'),
    path('product_detail/<int:product_id>', views.ProductView.as_view(), name='product_detail'),
    path('add_product_to_basket/<int:product_id>', views.add_product_to_basket, name='add_product'),
    path('delete_product_from_basket/<int:product_id>', views.delete_product_from_basket, name='delete_product'),
]

urlpatterns = [
    path('', views.IndexView.as_view(), name='start_page'),
    path('products_by_categories/', views.ProductsByCategoriesView.as_view(), name='products_by_categories'),
    path('products_by_categories/<str:category>/', views.ProductsByCategoriesView.as_view(), name='products_by_categories_plus'),
    path('basket/', views.BasketView.as_view(), name='basket'),
    path('salesman/<str:shop>', views.SalesmanView.as_view(), name='salesman'),
    path('', include(url_lists)),
    path('', include(url_orders)),
    path('', include(url_products)),
    path('', include(url_jsons)),
]

